"""Quick test script for MainAgent initialization"""
from agents.src.main_agent.main_agent import MainAgent

print("Testing MainAgent initialization...")
agent = MainAgent()
print("MainAgent initialized successfully!")
print(f"Agents loaded: {len(agent.agent_registry)}")

stats = agent.get_statistics()
print(f"\nStatistics:")
print(f"  Total agents: {stats['total_agents']}")
print(f"  Active agents: {stats['active_agents']}")

print("\nAvailable agents:")
for agent_info in stats['agents']:
    print(f"  - {agent_info['name']} ({agent_info['status']})")
    print(f"    Capabilities: {agent_info['capabilities']}")
    print(f"    Tools: {agent_info['tools']}, Skills: {agent_info['skills']}")

print("\nTest completed successfully!")

# Made with Bob
