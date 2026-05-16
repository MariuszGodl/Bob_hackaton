import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.sse import sse_client

from agents.src.models.mcp_server_model import MCPConnection
from agents.src.models.tool_model import ToolDefinition
from agents.src.models.skill_model import Skill


class CustomAgent(ABC):
    """
    Abstract Base Class for multi-turn agents managing MCP routing,
    skills registration, and runtime execution loops.
    """
    def __init__(
        self,
        system_prompt: str,
        skills: Optional[List[Skill]] = None,
        mcp_servers: Optional[List[MCPConnection]] = None,
        tools: Optional[List[ToolDefinition]] = None
    ):
        self.system_prompt = system_prompt
        self.skills = skills or []
        self.mcp_servers = mcp_servers or []
        self.tool_registry: Dict[str, ToolDefinition] = {t.name: t for t in (tools or [])}

    @abstractmethod
    async def _execute_inference(self, chat_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract method implemented by subclasses to hit specific model clients."""
        pass

    async def run(self, user_query: str) -> Optional[str]:
        sessions: Dict[str, ClientSession] = {}
        
        async with AsyncExitStack() as stack:
            # Connect to all SSE MCP Servers dynamically
            for server_info in self.mcp_servers:
                print(f"Connecting to {server_info.name} at {server_info.url}...")
                read_stream, write_stream = await stack.enter_async_context(sse_client(server_info.url))
                session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
                await session.initialize()
                
                sessions[server_info.name] = session
                
                mcp_tools_response = await session.list_tools()
                for t in mcp_tools_response.tools:
                    mcp_tool = ToolDefinition(
                        name=t.name,
                        description=t.description,
                        parameters=t.inputSchema,
                        source=server_info.name
                    )
                    self.tool_registry[mcp_tool.name] = mcp_tool
                    
            for skill in self.skills:
                tool = skill.to_tool()
                self.tool_registry[tool.name] = tool

            all_tools = [tool.to_watsonx_schema() for tool in self.tool_registry.values()]

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            chat_kwargs = {"messages": messages}
            if all_tools:
                chat_kwargs["tools"] = all_tools
            
            # First Model Call
            print("Chat arguments sent to LLM:", chat_kwargs)
            response = await self._execute_inference(chat_kwargs)
            
            message_obj = response["choices"][0]["message"]
            tool_calls = message_obj.get("tool_calls", [])
            
            if not tool_calls:
                print("Final Answer:\n", message_obj["content"])
                return message_obj["content"]

            for tc in tool_calls:
                tc["type"] = "function"
                
            messages.append({"role": "assistant", "tool_calls": tool_calls})
            
            # Execute Tools on the Correct Server/Environment
            for tc in tool_calls:
                name = tc['function']['name']
                args = json.loads(tc['function']['arguments'])
                
                tool_def = self.tool_registry.get(name)
                if not tool_def:
                    raise ValueError(f"Tool '{name}' not found in registry")
                
                if tool_def.source == "local":
                    if not tool_def.callable_func:
                        raise ValueError(f"Local tool '{name}' has no callable function")
                    result_text = str(tool_def.callable_func(**args))
                else:
                    target_session = sessions[tool_def.source]
                    mcp_res = await target_session.call_tool(name, args)
                    result_text = mcp_res.content[0].text
                
                msg = {"role": "tool", "tool_call_id": tc["id"], "content": result_text}
                print(f"Tool '{name}' called with result:", msg)
                messages.append(msg)
            
            # Second Model Call (Get final answer)
            final_response = await self._execute_inference(chat_kwargs)
            return final_response["choices"][0]["message"]["content"]


