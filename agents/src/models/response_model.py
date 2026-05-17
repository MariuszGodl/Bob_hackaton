from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal


@dataclass
class ResponseDataclass:
    """
    Standardized response format for all agent communications.
    Ensures consistent data flow between agents and provides tracking capabilities.
    """
    # Response status
    status: Literal["success", "error", "partial"] = "success"
    
    # Main response data
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Execution metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Error information (if any)
    errors: Optional[List[Dict[str, Any]]] = None
    
    # Agent execution chain for tracking
    agent_chain: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate the response structure."""
        if self.status not in ["success", "error", "partial"]:
            raise ValueError(f"Invalid status: {self.status}. Must be 'success', 'error', or 'partial'")
        
        # Ensure errors is a list if status is error
        if self.status == "error" and not self.errors:
            self.errors = []
    
    def add_agent_to_chain(self, agent_name: str) -> None:
        """Add an agent to the execution chain."""
        self.agent_chain.append(agent_name)
    
    def add_error(self, error_message: str, error_type: str = "general", **kwargs) -> None:
        """Add an error to the errors list."""
        if self.errors is None:
            self.errors = []
        
        error_dict = {
            "message": error_message,
            "type": error_type,
            **kwargs
        }
        self.errors.append(error_dict)
        
        # Update status if not already error
        if self.status == "success":
            self.status = "error"
    
    def merge_metadata(self, new_metadata: Dict[str, Any]) -> None:
        """Merge new metadata into existing metadata."""
        self.metadata.update(new_metadata)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        return {
            "status": self.status,
            "data": self.data,
            "metadata": self.metadata,
            "errors": self.errors,
            "agent_chain": self.agent_chain
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResponseDataclass":
        """Create a ResponseDataclass from a dictionary."""
        return cls(
            status=data.get("status", "success"),
            data=data.get("data", {}),
            metadata=data.get("metadata", {}),
            errors=data.get("errors"),
            agent_chain=data.get("agent_chain", [])
        )
    
    @classmethod
    def create_error_response(
        cls,
        error_message: str,
        agent_name: str,
        error_type: str = "general",
        **kwargs
    ) -> "ResponseDataclass":
        """Create an error response quickly."""
        response = cls(
            status="error",
            errors=[{
                "message": error_message,
                "type": error_type,
                **kwargs
            }],
            agent_chain=[agent_name]
        )
        return response
    
    @classmethod
    def create_success_response(
        cls,
        data: Dict[str, Any],
        agent_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "ResponseDataclass":
        """Create a success response quickly."""
        response = cls(
            status="success",
            data=data,
            metadata=metadata or {},
            agent_chain=[agent_name]
        )
        return response

# Made with Bob
