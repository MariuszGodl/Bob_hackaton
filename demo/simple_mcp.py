"""Simple MCP Server with get_current_location tool"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Create server instance
server = Server("simple-location-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_current_location",
            description="Returns the current location",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    if name == "get_current_location":
        return [TextContent(type="text", text="gdansk")]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# Made with Bob
