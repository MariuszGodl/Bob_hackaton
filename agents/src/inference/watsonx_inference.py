import json
import asyncio
import os
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from mcp import ClientSession
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack

from agents.src.models.mcp_server_model import MCPConnection
from agents.src.models.tool_model import ToolDefinition
from agents.src.models.skill_model import Skill


from typing import Dict, List, Optional

api_url = os.getenv("WATSONX_URL")
api_key = os.getenv("WATSONX_API_KEY")
api_project_id = os.getenv("WATSONX_PROJECT_ID")

if not api_url or not api_key or not api_project_id:
    raise ValueError("Error: WATSONX_URL, WATSONX_API_KEY, and WATSONX_PROJECT_ID environment variables must be set.")

# 1. Setup WatsonX Client & Model
client = APIClient(Credentials(
    url=api_url,
    api_key=api_key
))

model = ModelInference(
    model_id="mistral-large-2512",
    api_client=client,
    project_id=api_project_id,
    params={"time_limit": 10000, "max_tokens": 300}
)


async def chat(
    servers_info: Optional[List[MCPConnection]] = None, 
    tool_registry: Optional[Dict[str, ToolDefinition]] = None,
    skills: Optional[List[Skill]] = None,
    system_prompt: Optional[str] = None,
    user_query: str = "What is the capital of France?"
):
    if servers_info is None:
        servers_info = []
    if tool_registry is None:
        tool_registry = {}
    if skills is None:
        skills = []

    sessions: Dict[str, ClientSession] = {}
    
    # 3. Connect to all SSE MCP Servers dynamically
    async with AsyncExitStack() as stack:
        
        for server_info in servers_info:
            print(f"Connecting to {server_info.name} at {server_info.url}...")
            read_stream, write_stream = await stack.enter_async_context(sse_client(server_info.url))
            session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
            await session.initialize()
            
            # Store the session for later routing
            sessions[server_info.name] = session
            
            # 4. Merge MCP Tools for this specific server
            mcp_tools_response = await session.list_tools()
            for t in mcp_tools_response.tools:
                mcp_tool = ToolDefinition(
                    name=t.name,
                    description=t.description,
                    parameters=t.inputSchema,
                    source=server_info.name # Map tool to its specific server
                )
                tool_registry[mcp_tool.name] = mcp_tool
                
        for skill in skills:
            tool = skill.to_tool()
            tool_registry[tool.name] = tool

        
        # Prepare all tools for WatsonX
        all_tools = [tool.to_watsonx_schema() for tool in tool_registry.values()]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # Build kwargs dictionary so we ONLY pass tools if they exist
        chat_kwargs = {"messages": messages}
        if all_tools:
            chat_kwargs["tools"] = all_tools
        
        # 5. First Model Call
        print(chat_kwargs)
        response = model.chat(**chat_kwargs)
        tool_calls = response["choices"][0]["message"].get("tool_calls", [])
        
        if not tool_calls:
            print("Final Answer:\n", response["choices"][0]["message"]["content"])
            return

        # Ensure 'type' is set for each tool call
        for tc in tool_calls:
            tc["type"] = "function"
            
        messages.append({"role": "assistant", "tool_calls": tool_calls})
        
        # 6. Execute Tools on the Correct Server
        for tc in tool_calls:
            name = tc['function']['name']
            args = json.loads(tc['function']['arguments'])
            
            tool_def = tool_registry.get(name)
            
            if not tool_def:
                raise ValueError(f"Tool '{name}' not found in registry")
            
            if tool_def.source == "local":
                if not tool_def.callable_func:
                    raise ValueError(f"Local tool '{name}' has no callable function")
                result_text = str(tool_def.callable_func(**args))
            else:
                # Route to the exact session that owns this tool
                target_session = sessions[tool_def.source]
                mcp_res = await target_session.call_tool(name, args)
                result_text = mcp_res.content[0].text
            
            msg = {"role": "tool", "tool_call_id": tc["id"], "content": result_text}
            print(f"Tool '{name}' called with result:", msg)
            messages.append(msg)
        
        # 7. Second Model Call (Get final answer)
        # chat_kwargs still points to 'messages', which has now been appended with the tool results
        final_response = model.chat(**chat_kwargs)
        return final_response["choices"][0]["message"]["content"]
