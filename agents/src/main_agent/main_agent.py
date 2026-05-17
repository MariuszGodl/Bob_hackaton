"""
MainAgent - Central routing agent for multi-agent system.
Analyzes user queries and routes them to appropriate custom agents.
"""
import json
import os
import importlib
from typing import Dict, List, Optional, Any
from pathlib import Path

from agents.src.models.agent_model import AgentDataclass
from agents.src.models.response_model import ResponseDataclass


class MainAgent:
    """
    Main Agent that routes queries to appropriate custom agents.
    Manages agent registry, query classification, and response aggregation.
    """
    
    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the MainAgent with agent registry.
        
        Args:
            registry_path: Path to agent_registry.json. If None, uses default path.
        """
        if registry_path is None:
            # Default path relative to this file
            base_path = Path(__file__).parent.parent.parent
            self.registry_path = base_path / "config" / "agent_registry.json"
        else:
            self.registry_path = Path(registry_path)
        self.agent_registry: Dict[str, AgentDataclass] = {}
        self.active_agents: Dict[str, Any] = {}  # Cached agent instances
        
        # Load the registry
        self._load_registry()
        
        print(f"MainAgent initialized with {len(self.agent_registry)} agents")
    
    def _load_registry(self) -> None:
        """Load agent registry from JSON file."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Agent registry not found at {self.registry_path}")
        
        with open(self.registry_path, 'r') as f:
            registry_data = json.load(f)
        
        # Parse agents from registry
        for agent_data in registry_data.get("agents", []):
            agent = AgentDataclass.from_dict(agent_data)
            self.agent_registry[agent.agent_name] = agent
            print(f"  - Loaded: {agent.agent_name} ({agent.status})")
    
    def _get_agent_instance(self, agent_name: str) -> Any:
        """
        Get or create an instance of the specified agent.
        
        Args:
            agent_name: Name of the agent to instantiate
            
        Returns:
            Agent instance
        """
        # Check if already cached
        if agent_name in self.active_agents:
            return self.active_agents[agent_name]
        
        # Get agent metadata
        agent_meta = self.agent_registry.get(agent_name)
        if not agent_meta:
            raise ValueError(f"Agent '{agent_name}' not found in registry")
        
        if not agent_meta.is_active():
            raise ValueError(f"Agent '{agent_name}' is not active (status: {agent_meta.status})")
        
        # Dynamically import and instantiate the agent
        try:
            module = importlib.import_module(agent_meta.agent_module)
            agent_class = getattr(module, agent_meta.agent_class)
            
            # Instantiate with config from registry
            agent_instance = agent_class(**agent_meta.config)
            
            # Cache the instance
            self.active_agents[agent_name] = agent_instance
            
            return agent_instance
            
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate agent '{agent_name}': {e}")
    
    def _route_query(self, query: str) -> AgentDataclass:
        """
        Determine which agent should handle the query.
        
        This is a simple keyword-based routing. In production, this could use
        an LLM for more sophisticated routing.
        
        Args:
            query: User query string
            
        Returns:
            AgentDataclass for the selected agent
        """
        query_lower = query.lower()
        
        # Score each agent based on capability matching
        scores: Dict[str, int] = {}
        
        for agent_name, agent_meta in self.agent_registry.items():
            if not agent_meta.is_active():
                continue
            
            score = 0
            
            # Check capabilities
            for capability in agent_meta.capabilities:
                if capability.lower() in query_lower:
                    score += 10
            
            # Check tools
            for tool in agent_meta.available_tools:
                if tool.lower().replace("_", " ") in query_lower:
                    score += 5
            
            # Check skills
            for skill in agent_meta.available_skills:
                if skill.lower().replace("_", " ") in query_lower:
                    score += 5
            
            # Add priority bonus
            score += agent_meta.priority
            
            scores[agent_name] = score
        
        # Select agent with highest score
        if not scores:
            raise ValueError("No active agents available")
        
        best_agent_name = max(scores, key=lambda k: scores[k])
        best_score = scores[best_agent_name]
        
        # If no good match found (score is just priority), use default
        if best_score <= 10:  # Only priority, no capability match
            # Use the agent with highest priority as default
            best_agent_name = max(
                self.agent_registry.keys(),
                key=lambda name: self.agent_registry[name].priority
                if self.agent_registry[name].is_active() else -1
            )
        
        print(f"Routing query to: {best_agent_name} (score: {scores.get(best_agent_name, 0)})")
        return self.agent_registry[best_agent_name]
    
    async def process_query(self, query: str, agent_name: Optional[str] = None) -> ResponseDataclass:
        """
        Main entry point for processing user queries.
        
        Args:
            query: User query string
            agent_name: Optional specific agent to use. If None, routes automatically.
            
        Returns:
            ResponseDataclass with the result
        """
        try:
            # Step 1: Select agent
            if agent_name:
                if agent_name not in self.agent_registry:
                    return ResponseDataclass.create_error_response(
                        error_message=f"Agent '{agent_name}' not found in registry",
                        agent_name="main_agent",
                        error_type="agent_not_found"
                    )
                selected_agent_meta = self.agent_registry[agent_name]
            else:
                selected_agent_meta = self._route_query(query)
            
            # Step 2: Get agent instance
            agent_instance = self._get_agent_instance(selected_agent_meta.agent_name)
            
            # Step 3: Execute agent
            print(f"\nExecuting agent: {selected_agent_meta.agent_name}")
            print(f"Query: {query}\n")
            
            result = await agent_instance.run(query)
            
            # Step 4: Create response
            response = ResponseDataclass.create_success_response(
                data={"result": result},
                agent_name="main_agent",
                metadata={
                    "selected_agent": selected_agent_meta.agent_name,
                    "agent_version": selected_agent_meta.version,
                    "routing_method": "manual" if agent_name else "automatic"
                }
            )
            
            # Add the custom agent to the chain
            response.add_agent_to_chain(selected_agent_meta.agent_name)
            
            return response
            
        except Exception as e:
            print(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            
            return ResponseDataclass.create_error_response(
                error_message=str(e),
                agent_name="main_agent",
                error_type=type(e).__name__,
                traceback=traceback.format_exc()
            )
    
    def list_agents(self) -> List[AgentDataclass]:
        """Get list of all registered agents."""
        return list(self.agent_registry.values())
    
    def get_agent_info(self, agent_name: str) -> Optional[AgentDataclass]:
        """Get information about a specific agent."""
        return self.agent_registry.get(agent_name)
    
    def reload_registry(self) -> None:
        """Reload the agent registry from file."""
        self.agent_registry.clear()
        self.active_agents.clear()
        self._load_registry()
        print("Agent registry reloaded")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the agent system."""
        total_agents = len(self.agent_registry)
        active_agents = sum(1 for a in self.agent_registry.values() if a.is_active())
        cached_agents = len(self.active_agents)
        
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "cached_agents": cached_agents,
            "agents": [
                {
                    "name": agent.agent_name,
                    "status": agent.status,
                    "capabilities": len(agent.capabilities),
                    "tools": len(agent.available_tools),
                    "skills": len(agent.available_skills)
                }
                for agent in self.agent_registry.values()
            ]
        }

# Made with Bob
