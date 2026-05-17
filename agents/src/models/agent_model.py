from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class AgentDataclass:
    """
    Metadata for agent registration and discovery.
    Used by the MainAgent to route queries to appropriate custom agents.
    """
    # Basic identification
    agent_name: str
    agent_class: str  # Python class name (e.g., "WatsonXAgent")
    agent_module: str  # Python module path (e.g., "agents.usage.custom_agents.watsons_agent")
    
    # Description and capabilities
    description: str
    capabilities: List[str] = field(default_factory=list)  # List of domains/tasks
    
    # Available resources
    available_tools: List[str] = field(default_factory=list)
    available_mcp_servers: List[str] = field(default_factory=list)
    available_skills: List[str] = field(default_factory=list)
    
    # Subagents this agent can delegate to
    subagents: List[str] = field(default_factory=list)  # List of agent names
    
    # Metadata
    version: str = "1.0.0"
    status: str = "active"  # active, inactive, maintenance
    priority: int = 0  # Higher priority agents are preferred for routing
    
    # Optional configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate agent metadata."""
        if not self.agent_name:
            raise ValueError("agent_name is required")
        if not self.agent_class:
            raise ValueError("agent_class is required")
        if not self.agent_module:
            raise ValueError("agent_module is required")
        if not self.description:
            raise ValueError("description is required")
        
        # Validate status
        valid_statuses = ["active", "inactive", "maintenance"]
        if self.status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")
    
    def is_active(self) -> bool:
        """Check if the agent is active and available."""
        return self.status == "active"
    
    def can_handle_capability(self, capability: str) -> bool:
        """Check if this agent can handle a specific capability."""
        return capability.lower() in [c.lower() for c in self.capabilities]
    
    def has_tool(self, tool_name: str) -> bool:
        """Check if this agent has a specific tool."""
        return tool_name in self.available_tools
    
    def has_skill(self, skill_name: str) -> bool:
        """Check if this agent has a specific skill."""
        return skill_name in self.available_skills
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "agent_name": self.agent_name,
            "agent_class": self.agent_class,
            "agent_module": self.agent_module,
            "description": self.description,
            "capabilities": self.capabilities,
            "available_tools": self.available_tools,
            "available_mcp_servers": self.available_mcp_servers,
            "available_skills": self.available_skills,
            "subagents": self.subagents,
            "version": self.version,
            "status": self.status,
            "priority": self.priority,
            "config": self.config
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentDataclass":
        """Create AgentDataclass from dictionary."""
        return cls(
            agent_name=data["agent_name"],
            agent_class=data["agent_class"],
            agent_module=data["agent_module"],
            description=data["description"],
            capabilities=data.get("capabilities", []),
            available_tools=data.get("available_tools", []),
            available_mcp_servers=data.get("available_mcp_servers", []),
            available_skills=data.get("available_skills", []),
            subagents=data.get("subagents", []),
            version=data.get("version", "1.0.0"),
            status=data.get("status", "active"),
            priority=data.get("priority", 0),
            config=data.get("config", {})
        )
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the agent."""
        return (
            f"{self.agent_name} (v{self.version})\n"
            f"Status: {self.status}\n"
            f"Description: {self.description}\n"
            f"Capabilities: {', '.join(self.capabilities)}\n"
            f"Tools: {len(self.available_tools)}, "
            f"Skills: {len(self.available_skills)}, "
            f"MCP Servers: {len(self.available_mcp_servers)}"
        )

# Made with Bob
