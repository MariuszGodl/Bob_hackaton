import json
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, Optional, Literal

@dataclass
class ToolDefinition:
    """
    Contains everything required to define a tool for an LLM and execute it.
    """
    # 1. LLM Required Information
    name: str
    description: str
    parameters: Dict[str, Any]
    
    # 2. Execution Information
    source: Literal["local", "mcp"] = "local"
    
    # For local tools: the actual Python function to run
    callable_func: Optional[Callable] = None 
    
    # For MCP tools: optional metadata (like which server it belongs to)
    server_name: Optional[str] = None

    def to_watsonx_schema(self) -> Dict[str, Any]:
        """
        Converts the dataclass into the standard OpenAI/Watsonx tool schema.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    async def execute(self, arguments: Dict[str, Any], mcp_session=None) -> str:
        """
        Executes the tool automatically routing it based on its source.
        Always returns a string representation of the result.
        """
        if self.source == "local":
            if not self.callable_func:
                raise ValueError(f"Local tool '{self.name}' has no callable function attached.")
            
            # Handle both async and sync local functions
            if asyncio.iscoroutinefunction(self.callable_func):
                result = await self.callable_func(**arguments)
            else:
                result = self.callable_func(**arguments)
                
            return str(result)
            
        elif self.source == "mcp":
            if not mcp_session:
                raise RuntimeError(f"Cannot execute MCP tool '{self.name}' without an active mcp_session.")
            
            # Call the MCP server and extract the text content
            mcp_response = await mcp_session.call_tool(self.name, arguments)
            return mcp_response.content[0].text
            
        else:
            raise ValueError(f"Unknown tool source: {self.source}")