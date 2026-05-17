"""
Demo script for testing the MainAgent with automatic routing.
This demonstrates how the MainAgent routes queries to appropriate custom agents.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.src.main_agent.main_agent import MainAgent


async def main():
    """
    Test the MainAgent with various queries.
    """
    print("=" * 80)
    print("MainAgent Demo - Automatic Query Routing")
    print("=" * 80)
    print()
    
    # Initialize MainAgent
    try:
        main_agent = MainAgent()
        print("\n✓ MainAgent initialized successfully!")
        print()
    except Exception as e:
        print(f"✗ Error initializing MainAgent: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Display agent statistics
    stats = main_agent.get_statistics()
    print("Agent System Statistics:")
    print(f"  Total agents: {stats['total_agents']}")
    print(f"  Active agents: {stats['active_agents']}")
    print()
    
    # Display available agents
    print("Available Agents:")
    for agent in main_agent.list_agents():
        print(f"\n  {agent.agent_name}:")
        print(f"    Status: {agent.status}")
        print(f"    Description: {agent.description}")
        print(f"    Capabilities: {', '.join(agent.capabilities[:5])}")
        if len(agent.capabilities) > 5:
            print(f"                  ... and {len(agent.capabilities) - 5} more")
    print()
    print("=" * 80)
    
    # Test queries
    test_queries = [
        {
            "name": "Text Statistics",
            "query": "Calculate the word count for this sentence: 'The quick brown fox jumps over the lazy dog.'",
            "description": "Should route to watsonx_general_agent and use text_stats tool"
        },
        {
            "name": "Date Calculation",
            "query": "How many days are between 2024-01-01 and 2024-12-31?",
            "description": "Should route to watsonx_general_agent and use date calculation"
        },
        {
            "name": "Code Review",
            "query": "Review this Python code for security issues: exec('print(hello)')",
            "description": "Should route to watsonx_general_agent and use code_review skill"
        },
        {
            "name": "General Question",
            "query": "What is IBM WatsonX and what can it do?",
            "description": "Should route to watsonx_general_agent for general assistance"
        },
        {
            "name": "Password Generation",
            "query": "Generate a secure password with 16 characters including special characters",
            "description": "Should route to watsonx_general_agent and use password tool"
        }
    ]
    
    # Interactive or batch mode
    print("\nSelect mode:")
    print("1. Interactive mode (enter your own queries)")
    print("2. Batch test mode (run predefined test queries)")
    print("3. Single query test")
    
    try:
        mode = input("\nEnter mode (1/2/3) [default: 3]: ").strip() or "3"
    except (EOFError, KeyboardInterrupt):
        mode = "3"
        print("3")
    
    if mode == "1":
        # Interactive mode
        print("\n" + "=" * 80)
        print("Interactive Mode - Enter 'quit' or 'exit' to stop")
        print("=" * 80)
        
        while True:
            try:
                user_query = input("\nYour query: ").strip()
                if user_query.lower() in ['quit', 'exit', 'q']:
                    print("Exiting...")
                    break
                
                if not user_query:
                    continue
                
                print("\n" + "-" * 80)
                response = await main_agent.process_query(user_query)
                print("-" * 80)
                
                print(f"\nStatus: {response.status}")
                print(f"Agent Chain: {' -> '.join(response.agent_chain)}")
                
                if response.status == "success":
                    print("\n✓ RESULT:")
                    print("=" * 80)
                    print(response.data.get("result", "No result"))
                    print("=" * 80)
                else:
                    print("\n✗ ERROR:")
                    print("=" * 80)
                    for error in response.errors or []:
                        print(f"  {error.get('type', 'error')}: {error.get('message', 'Unknown error')}")
                    print("=" * 80)
                
                print(f"\nMetadata: {response.metadata}")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()
    
    elif mode == "2":
        # Batch test mode
        print("\n" + "=" * 80)
        print("Batch Test Mode - Running all test queries")
        print("=" * 80)
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n{'=' * 80}")
            print(f"Test {i}/{len(test_queries)}: {test['name']}")
            print(f"Description: {test['description']}")
            print(f"Query: {test['query']}")
            print("=" * 80)
            
            try:
                response = await main_agent.process_query(test['query'])
                
                print(f"\nStatus: {response.status}")
                print(f"Agent Chain: {' -> '.join(response.agent_chain)}")
                print(f"Selected Agent: {response.metadata.get('selected_agent', 'unknown')}")
                
                if response.status == "success":
                    print("\n✓ RESULT:")
                    print("-" * 80)
                    print(response.data.get("result", "No result"))
                    print("-" * 80)
                else:
                    print("\n✗ ERROR:")
                    print("-" * 80)
                    for error in response.errors or []:
                        print(f"  {error.get('type', 'error')}: {error.get('message', 'Unknown error')}")
                    print("-" * 80)
                
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()
            
            # Pause between tests
            if i < len(test_queries):
                try:
                    input("\nPress Enter to continue to next test (or Ctrl+C to stop)...")
                except KeyboardInterrupt:
                    print("\n\nStopped by user.")
                    break
    
    else:
        # Single query test (default)
        print("\n" + "=" * 80)
        print("Single Query Test Mode")
        print("=" * 80)
        
        test = test_queries[0]  # Use first test query
        print(f"\nTest: {test['name']}")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['description']}")
        print("-" * 80)
        
        try:
            response = await main_agent.process_query(test['query'])
            
            print(f"\nStatus: {response.status}")
            print(f"Agent Chain: {' -> '.join(response.agent_chain)}")
            print(f"Selected Agent: {response.metadata.get('selected_agent', 'unknown')}")
            
            if response.status == "success":
                print("\n✓ RESULT:")
                print("=" * 80)
                print(response.data.get("result", "No result"))
                print("=" * 80)
            else:
                print("\n✗ ERROR:")
                print("=" * 80)
                for error in response.errors or []:
                    print(f"  {error.get('type', 'error')}: {error.get('message', 'Unknown error')}")
                print("=" * 80)
            
            print(f"\nMetadata: {response.metadata}")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("MainAgent Demo Complete")
    print("=" * 80)


if __name__ == "__main__":
    print("\nStarting MainAgent Demo...")
    print("Note: Make sure the WatsonX MCP server is running on http://127.0.0.1:8001/sse")
    print("      Run it with: python agents/usage/mcp_servers/ibm_watsonx_mcp.py")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
