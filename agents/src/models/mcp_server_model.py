from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class MCPConnection:
    """Represents an MCP Server connection and handles tool schema conversion."""
    name: str
    port: int
    host: str = "127.0.0.1"
    path: str = "sse"
    
    # Raw tools populated dynamically after connecting to the MCP Server
    mcp_tools: List[Any] = field(default_factory=list)

    @property
    def url(self) -> str:
        """Constructs the full SSE connection URL."""
        return f"http://{self.host}:{self.port}/{self.path.lstrip('/')}"
