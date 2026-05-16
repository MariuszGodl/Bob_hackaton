import os
import io
import contextlib
import uvicorn
from mcp.server.fastmcp import FastMCP
from ibm_watsonx_ai import APIClient, Credentials
from mcp.types import TextContent

# Initialize the FastMCP server
watsonx_mcp_server = FastMCP("Watsonx_Models_Server")

@watsonx_mcp_server.tool()
def get_watsonx_chat_models() -> list[TextContent]:
    """
    Retrieves the available chat models from IBM watsonx.ai.
    Returns a formatted table of supported foundation models.
    """
    # Fetch credentials from environment variables or use the provided fallbacks
    api_url = os.getenv("WATSONX_URL")
    api_key = os.getenv("WATSONX_API_KEY")
    
    if not api_url or not api_key:
        raise Exception("Error: WATSONX_URL and WATSONX_API_KEY environment variables must be set.")

    # Initialize credentials
    credentials = Credentials(
        url=api_url,
        api_key=api_key
    )
    
    # Authenticate the API Client
    api_client = APIClient(credentials)
    
    # Because .show() prints directly to standard output, we need to intercept it 
    # using contextlib so the MCP tool can return the text directly to the LLM.
    captured_output = io.StringIO()
    with contextlib.redirect_stdout(captured_output):
        api_client.foundation_models.ChatModels.show()
    
    result = captured_output.getvalue()
    
    if not result.strip():
        return [TextContent(type="text", text="Warning: No models returned or output could not be captured.")]
        
    return [TextContent(type="text", text=result)]


if __name__ == "__main__":
    # 1. Extract the network (ASGI) application from the FastMCP server
    app = watsonx_mcp_server.sse_app()
    
    # 2. Run the application locally on the desired host and port using uvicorn
    print("Starting Watsonx MCP Server on http://127.0.0.1:8001/sse")
    uvicorn.run(app, host="127.0.0.1", port=8001)