import json
import asyncio
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os

api_url = os.getenv("WATSONX_URL")
api_key = os.getenv("WATSONX_API_KEY")
api_project_id = os.getenv("WATSONX_PROJECT_ID")

if not api_url or not api_key or not api_project_id:
    raise ValueError("Error: WATSONX_URL and WATSONX_API_KEY, WATSONX_PROJECT_ID environment variables must be set.")

# 1. Setup WatsonX Client & Model
client = APIClient(Credentials(
    url=api_url,
    api_key=api_key
))

model = ModelInference(
    model_id="mistral-large-2512",
    api_client=client,
    project_id=api_project_id,
    params={"time_limit": 10000, "max_tokens": 300}
)

# 2. Define Local Tool
def multiply(a: float, b: float) -> float: 
    return float(a) * float(b)

local_tool = {
    "type": "function",
    "function": {
        "name": "multiply",
        "description": "Multiply two numbers",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"]
        }
    }
}

async def main():
    server_params = StdioServerParameters(command="python", args=["demo/simple_mcp.py"])
    
    # 3. Connect to MCP Server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # 4. Merge Local and MCP Tools
            mcp_tools_response = await session.list_tools()
            tools = [local_tool] + [
                {
                    "type": "function", 
                    "function": {"name": t.name, "description": t.description, "parameters": t.inputSchema}
                } for t in mcp_tools_response.tools
            ]
            
            messages = [{"role": "user", "content": "What is 15 multiplied by 7? Also, what is my current location?"}]
            
            # 5. First Model Call (Ask for tool calls)
            response = model.chat(messages=messages, tools=tools)
            tool_calls = response["choices"][0]["message"].get("tool_calls", [])
            
            # ---> FIX HERE: Ensure 'type' is set for each tool call <---
            for tc in tool_calls:
                tc["type"] = "function"
                
            messages.append({"role": "assistant", "tool_calls": tool_calls})
            
            # 6. Execute Tools
            for tc in tool_calls:
                name = tc['function']['name']
                
                args = json.loads(tc['function']['arguments'])
                
                if name == "multiply":
                    result_text = str(multiply(**args))
                else:
                    mcp_res = await session.call_tool(name, args)
                    # Extract the text specifically based on MCP TextContent structure
                    result_text = mcp_res.content[0].text
                
                # Note: changed role from 'tool' to 'user' or properly formatted 'tool' msg depending on what WatsonX requires. 
                # Usually standard chat schema requires "role": "tool".
                msg = {"role": "tool", "tool_call_id": tc["id"], "content": result_text}
                print("Tool call result:", msg)
                messages.append(msg)
            
            # 7. Second Model Call (Get final answer)
            final_response = model.chat(messages=messages, tools=tools)
            print("Final Answer:\n", final_response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())