from dataclasses import dataclass
import re
from agents.src.models.tool_model import ToolDefinition

@dataclass
class Skill:
    """Represents a specific skill with its full details and a brief summary."""
    name: str
    full_content: str
    short_description: str

    def __post_init__(self):
        """Enforces the 100-character limit for the summary."""
        if len(self.short_description) > 100:
            self.short_description = self.short_description[:97] + "..."

    def to_tool(self) -> ToolDefinition:
        """
        Converts the skill into a parameter-less ToolDefinition so the 
        LLM can request the full_content dynamically.
        """
        # LLMs require tool names to be alphanumeric with underscores/hyphens.
        # "Speak Like Eminem" -> "speak_like_eminem"
        safe_tool_name = re.sub(r'[^a-zA-Z0-9_-]', '_', self.name).lower()
        
        return ToolDefinition(
            name=f"read_skill_{safe_tool_name}",
            # We put the short description inside the tool description so the LLM 
            # knows exactly what it will get by calling this tool!
            description=f"Read the full, detailed instructions for the skill: {self.name}. Summary: {self.short_description}",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            },
            source="local",
            # The callable function just returns the string of the full content
            callable_func=lambda: self.full_content 
        )