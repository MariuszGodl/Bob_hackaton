import json
import asyncio
import os
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from mcp import ClientSession
from mcp.client.sse import sse_client
import sys
from pathlib import Path
from contextlib import AsyncExitStack

# Assuming these imports work in your local environment
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.usage.mcp_servers.ibm_watsonx_mcp import watsonx_mcp_server
from agents.src.models.mcp_server_model import MCPConnection
from agents.src.models.tool_model import ToolDefinition
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

local_tool_registry: Dict[str, ToolDefinition] = {}

# Register a Local Tool
def multiply(a: float, b: float) -> float: 
    return float(a) * float(b)

local_tool = ToolDefinition(
    name="multiply",
    description="Multiply two numbers",
    parameters={
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"]
    },
    source="local",
    callable_func=multiply
)
local_tool_registry[local_tool.name] = local_tool


# 2. Make arguments optional with defaults
async def main(
    servers_info: Optional[List[MCPConnection]] = None, 
    tool_registry: Optional[Dict[str, ToolDefinition]] = None
):
    if servers_info is None:
        servers_info = []
    if tool_registry is None:
        tool_registry = {}

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
                
        # Prepare all tools for WatsonX
        all_tools = [tool.to_watsonx_schema() for tool in tool_registry.values()]
        
        messages = [{"role": "user", "content": "What is 15 multiplied by 7? Also, what is my current location? Also what are models of watsonx"}]
        
        # Build kwargs dictionary so we ONLY pass tools if they exist
        chat_kwargs = {"messages": messages}
        if all_tools:
            chat_kwargs["tools"] = all_tools
        
        # 5. First Model Call
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
            
            if tool_def.source == "local":
                result_text = str(multiply(**args))
            else:
                # Route to the exact session that owns this tool
                target_session = sessions[tool_def.source]
                mcp_res = await target_session.call_tool(name, args)
                result_text = mcp_res.content[0].text
            
            msg = {"role": "tool", "tool_call_id": tc["id"], "content": result_text}
            print("Tool call result:", msg)
            messages.append(msg)
        
        # 7. Second Model Call (Get final answer)
        # chat_kwargs still points to 'messages', which has now been appended with the tool results
        final_response = model.chat(**chat_kwargs)
        print("Final Answer:\n", final_response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    location_server = MCPConnection(name="Location_Server", port=8000)
    watsonx_mcp_server = MCPConnection(name="Watsonx_Models_Server", port=8001)
    
    print("--- Running WITH servers and tools ---")
    asyncio.run(main([location_server, watsonx_mcp_server], local_tool_registry.copy()))
    
    print("\n--- Running WITHOUT servers or tools (LLM Only) ---")
    asyncio.run(main())