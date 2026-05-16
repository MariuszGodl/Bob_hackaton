"""Simple MCP Server with get_current_location tool using FastMCP and SSE"""
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Initialize the FastMCP server
location_mcp_server = FastMCP("Simple_Location_Server")

@location_mcp_server.tool()
def get_current_location() -> list[TextContent]:
    """
    Returns the current location.
    """
    return [TextContent(type="text", text="gdansk")]

if __name__ == "__main__":
    # 1. Extract the network (ASGI) application from the FastMCP server
    app = location_mcp_server.sse_app()
    
    # 2. Run the application locally on the desired host and port using uvicorn
    print("Starting Location MCP Server on http://127.0.0.1:8000/sse")
    uvicorn.run(app, host="127.0.0.1", port=8000)