import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run_client():
    # The URL matches the host and port defined in your server.py
    server_url = "http://127.0.0.1:8000/sse"
    print(f"Connecting to running MCP server at {server_url}...")
    
    try:
        # Connect to the already running server via HTTP/SSE
        async with sse_client(url=server_url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection handshake
                await session.initialize()
                
                print("Connected successfully!\n")
                
                # Call the specific tool
                print("Calling 'get_watsonx_chat_models'...")
                result = await session.call_tool(
                    name="get_watsonx_chat_models", 
                    arguments={}
                )
                
                # Print out the response content
                print("\n--- Server Response ---")
                for content in result.content:
                    if hasattr(content, "text"):
                        print(content.text)
                    else:
                        print(content)
                        
    except Exception as e:
        print(f"\n[Client Error] Failed to communicate with MCP server: {e}")
        print("Ensure the server is running in another terminal.")

if __name__ == "__main__":
    asyncio.run(run_client())