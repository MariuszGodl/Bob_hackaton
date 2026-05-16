"""
Debug/Runner script for WatsonXAgent
This script demonstrates how to initialize and run the WatsonXAgent with all its capabilities.
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from agents.usage.custom_agents.watsons_agent import WatsonXAgent


async def main():
    """
    Main function to test the WatsonXAgent with various configurations.
    """
    print("=" * 80)
    print("WatsonX Agent Debugger/Runner")
    print("=" * 80)
    
    # Configuration options
    print("\nAgent Configuration:")
    print("- Default Skills: format_release_notes, code_review")
    print("- Default Tools: text_stats, date_diff, password_gen, url_parser, bmi_calc")
    print("- MCP Server: Watsonx_Models_Server (http://127.0.0.1:8001/sse)")
    print()
    
    # Initialize the agent with all default components
    try:
        agent = WatsonXAgent(
            system_prompt=(
                "You are an advanced AI assistant powered by IBM WatsonX. "
                "You have access to various tools, skills, and MCP servers to help users. "
                "Use the available tools when appropriate to provide accurate and helpful responses."
            ),
            include_default_skills=True,
            include_default_tools=True,
            include_watsonx_mcp=True
        )
        print("✓ Agent initialized successfully!")
        print(f"  - Skills loaded: {len(agent.skills)}")
        print(f"  - Tools loaded: {len(agent.tool_registry)}")
        print(f"  - MCP servers configured: {len(agent.mcp_servers)}")
        print()
        
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test queries
    test_queries = [
        {
            "name": "Simple Query (No Tools)",
            "query": "What is IBM WatsonX?",
            "description": "Tests basic inference without tool calls"
        },
        {
            "name": "Text Statistics Tool",
            "query": "Calculate the word and character count for this text: 'Hello world, this is a test message.'",
            "description": "Tests the text statistics tool"
        },
        {
            "name": "Date Calculation Tool",
            "query": "How many days are between 2024-01-01 and 2024-12-31?",
            "description": "Tests the date difference calculator"
        },
        {
            "name": "Password Generation Tool",
            "query": "Generate a secure password with 16 characters including special characters.",
            "description": "Tests the password generator"
        },
        {
            "name": "Code Review Skill",
            "query": "Review this Python code for security issues: exec('print(hello)')",
            "description": "Tests the code review skill"
        },
        {
            "name": "MCP Server Query",
            "query": "What chat models are available in WatsonX?",
            "description": "Tests the WatsonX MCP server (requires server to be running)"
        }
    ]
    
    # Interactive mode or batch mode
    print("Select mode:")
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
                print(f"Processing: {user_query}")
                print("-" * 80)
                
                result = await agent.run(user_query)
                
                print("\n" + "=" * 80)
                print("FINAL RESULT:")
                print("=" * 80)
                print(result)
                print("=" * 80)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"\n✗ Error processing query: {e}")
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
                result = await agent.run(test['query'])
                print("\n✓ RESULT:")
                print("-" * 80)
                print(result)
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
        
        test_query = "Calculate the word count for this sentence: 'The quick brown fox jumps over the lazy dog.'"
        print(f"\nTest Query: {test_query}")
        print("-" * 80)
        
        try:
            result = await agent.run(test_query)
            print("\n✓ RESULT:")
            print("=" * 80)
            print(result)
            print("=" * 80)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("WatsonX Agent Test Complete")
    print("=" * 80)


if __name__ == "__main__":
    print("\nStarting WatsonX Agent Runner...")
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
