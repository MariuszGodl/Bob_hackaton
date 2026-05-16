from agents.src.custom_agent.custom_agent import CustomAgent
from agents.src.inference.watsonx_inference import model
from agents.src.models.mcp_server_model import MCPConnection
from agents.src.models.skill_model import Skill
from agents.src.models.tool_model import ToolDefinition
from typing import Dict, Any, List, Optional

# Import the MCP server configuration
from agents.usage.mcp_servers.ibm_watsonx_mcp import watsonx_mcp_server

# Import skills
from agents.usage.skills.format_release_notes import format_release_notes
from agents.usage.skills.code_review import code_review_skill

# Import tools
from agents.usage.tools.math_tools import (
    text_stats_tool,
    date_diff_tool,
    password_tool,
    url_parser_tool,
    bmi_tool
)


class WatsonXAgent(CustomAgent):
    """
    Concrete Agent that leverages the imported WatsonX inference engine.
    Integrates with MCP servers, skills, and local tools for enhanced capabilities.
    """
    
    def __init__(
        self,
        system_prompt: str = "You are a helpful AI assistant powered by IBM WatsonX.",
        skills: Optional[List[Skill]] = None,
        mcp_servers: Optional[List[MCPConnection]] = None,
        tools: Optional[List[ToolDefinition]] = None,
        include_default_skills: bool = True,
        include_default_tools: bool = True,
        include_watsonx_mcp: bool = True
    ):
        """
        Initialize the WatsonXAgent with optional MCP servers, skills, and tools.
        
        Args:
            system_prompt: The system prompt for the agent
            skills: List of custom skills to add
            mcp_servers: List of MCP server connections
            tools: List of custom tool definitions
            include_default_skills: Whether to include default skills (format_release_notes, code_review)
            include_default_tools: Whether to include default math tools
            include_watsonx_mcp: Whether to include the WatsonX MCP server
        """
        # Prepare skills list
        final_skills = skills or []
        if include_default_skills:
            final_skills.extend([format_release_notes, code_review_skill])
        
        # Prepare tools list
        final_tools = tools or []
        if include_default_tools:
            final_tools.extend([
                text_stats_tool,
                date_diff_tool,
                password_tool,
                url_parser_tool,
                bmi_tool
            ])
        
        # Prepare MCP servers list
        final_mcp_servers = mcp_servers or []
        if include_watsonx_mcp:
            watsonx_mcp_connection = MCPConnection(
                name="Watsonx_Models_Server",
                port=8001,
            )
            final_mcp_servers.append(watsonx_mcp_connection)
        
        # Initialize the parent CustomAgent with all components
        super().__init__(
            system_prompt=system_prompt,
            skills=final_skills,
            mcp_servers=final_mcp_servers,
            tools=final_tools
        )
    
    async def _execute_inference(self, chat_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute inference using the WatsonX model.
        Uses the model object imported from agents.src.inference.watsonx_inference
        """
        return model.chat(**chat_kwargs)