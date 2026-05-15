
1) Inference Module

    1.1) Purpose:
        Core module that handles LLM interactions for all agents.
        Converts various tool formats to OpenAI standard and manages API calls.

    1.2) Input Parameters:
        - query: str | dict (user query)
        - tools: list[ToolDataclass] (custom tools)
        - mcp_servers: list[McpDataclass] (MCP server tools)
        - skills: list[SkillDataclass] (available skills)
        - system_prompt: str (agent-specific instructions)

    1.3) Implementation:

        class InferenceModule:
            def __init__(self, api_key: str):
                self.client = OpenAI(api_key=api_key)
            
            def execute(
                self,
                query: str | dict,
                tools: list[ToolDataclass],
                mcp_servers: list[McpDataclass],
                skills: list[SkillDataclass],
                system_prompt: str,
                **kwargs
            ) -> ResponseDataclass:
                """
                Main execution method:
                1. Convert all tools to OpenAI format
                2. Add skill descriptions (SKILLDATACLASS.short_description)
                3. Create skill retrieval tool
                4. Call IBM Watson Assistant API
                5. Handle tool calls
                6. Return standardized response
                """
                pass
            
            def _convert_tools_to_openai_format(
                self,
                tools: list[ToolDataclass],
                mcp_servers: list[McpDataclass]
            ) -> list[dict]:
                """
                Convert all tools (custom + MCP) to OpenAI function calling format.
                Each tool should have:
                - name
                - description
                - parameters (JSON schema)
                """
                pass
            
            
            def _handle_tool_calls(
                self,
                tool_calls: list,
                tools: list[ToolDataclass],
                mcp_servers: list[McpDataclass],
                skills: list[SkillDataclass]
            ) -> list[dict]:
                """
                Execute tool calls and return results.
                Handles:
                - Custom tool execution
                - MCP server tool calls
                - Skill retrieval
                - Error handling for failed tool calls
                """
                pass
            
            def _validate_response(self, response: dict) -> bool:
                """Validate LLM response format"""
                pass

    1.4) Tool Conversion Details:

        Custom Tool → OpenAI Format:
            ToolDataclass.openai_schema is already in correct format
        
        MCP Tool → OpenAI Format:
            Extract tool definitions from MCP server
            Convert to OpenAI function calling schema
        
        Skill → Tool:
            Create get_skill_instruction tool
            Only include skill names and short descriptions in context

    1.5) Error Handling:

        - API errors: Retry with exponential backoff
        - Tool execution errors: Return error message to LLM
        - Timeout: Return partial results if available
        - Invalid tool calls: Ask LLM to retry with correct format
        - Rate limits: Queue requests or return error

    1.6) Response Format:

        Returns ResponseDataclass:
            - status: "success" | "error" | "partial"
            - data: dict (LLM response and tool results)
            - metadata: dict (tokens used, cost, execution time, model used)
            - errors: list[dict] | None
            - agent_chain: list[str] (for tracking in multi-agent scenarios)

2) Custom Agent Class (Abstract Base)

    2.1) Purpose:
        Abstract base class that all custom agents inherit from.
        Provides standard interface for agent execution.

    2.2) Implementation:

        from abc import ABC, abstractmethod

        class CustomAgent(ABC):
            def __init__(
                self,
                agent_name: str,
                description: str,
                mcp_servers: list[MCPServerDataClass],
                tools: list[ToolDataclass],
                skills: list[SkillDataClass],
                subagents: list[AgentDataClass],
                custom_prompt: str,
                max_subagent_depth: int = 3
            ):
                self.agent_name = agent_name
                self.description = description
                self.mcp_servers = mcp_servers
                self.tools = tools
                self.skills = skills
                self.subagents = subagents
                self.custom_prompt = custom_prompt
                self.max_subagent_depth = max_subagent_depth
                self.inference_module = InferenceModule(api_key=os.getenv("IBM_API_KEY"))

            
            def run(self, query: str | dict, depth: int = 0) -> ResponseDataclass:
                """
                Main execution method for agent.
                
                Args:
                    query: User query (string or structured dict)
                    depth: Current recursion depth (for subagent calls)
                
                Returns:
                    ResponseDataclass with results
                
                Raises:
                    RecursionError: If max depth exceeded
                """
                if depth > self.max_subagent_depth:
                    raise RecursionError(f"Maximum subagent depth ({self.max_subagent_depth}) exceeded")
                
                try:
                    # Execute inference
                    response = self.inference_module.execute(
                        query=query,
                        tools=self.tools,
                        mcp_servers=self.mcp_servers,
                        skills=self.skills,
                        system_prompt=self._build_system_prompt()
                    )
                    
                    # Add agent to chain
                    response.agent_chain.append(self.agent_name)
                    
                    return response
                    
                except Exception as e:
                    return self._handle_error(e, depth)
            
            def _build_system_prompt(self) -> str:
                """
                Build complete system prompt including:
                - Custom prompt
                - Available subagents
                - General instructions
                """
                prompt = self.custom_prompt + "\n\n"
                
                if self.subagents:
                    prompt += "Available subagents:\n"
                    for subagent in self.subagents:
                        prompt += f"- {subagent.name}: {subagent.description}\n"
                    prompt += "\nYou can delegate tasks to subagents when appropriate.\n"
                
                return prompt
            
            def _handle_error(self, error: Exception, depth: int) -> ResponseDataclass:
                """Return standardized error response"""
                return ResponseDataclass(
                    status="error",
                    data={},
                    metadata={
                        "agent_name": self.agent_name,
                        "depth": depth,
                        "error_type": type(error).__name__
                    },
                    errors=[{"message": str(error)}],
                    agent_chain=[self.agent_name]
                )
            
            @abstractmethod
            def validate_dependencies(self) -> bool:
                """
                Validate that all required dependencies are available.
                Must be implemented by concrete agent classes.
                """
                pass

    2.3) Usage Example:

        class DataAnalystAgent(CustomAgent):
            def __init__(self):
                super().__init__(
                    agent_name="data_analyst",
                    description="Analyzes data and generates insights",
                    mcp_servers=[pandas_mcp_server],
                    tools=[plot_tool, statistics_tool],
                    skills=[data_cleaning_skill, visualization_skill],
                    subagents=[],
                    custom_prompt="You are a data analyst expert..."
                )
            
            def validate_dependencies(self) -> bool:
                # Check if pandas MCP server is available
                # Check if required tools are functional
                return True

3) Integration Notes:

    3.1) Inference Module + Custom Agent:
        - Custom agent uses inference module for all LLM interactions
        - Inference module is stateless and reusable
        - Each agent can configure inference parameters

    3.2) Tool Execution Flow:
        Query → Agent → Inference Module → OpenAI API → Tool Calls → Tool Execution → Response

    3.3) Skill Handling:
        - Skills are NOT included in full in the prompt (saves tokens)
        - Only skill names and short descriptions are included
        - LLM calls get_skill_instruction tool when it needs full skill content
        - This allows having many skills without context overflow

    3.4) Future Enhancements (Optional):
        - Streaming responses for long-running tasks
        - Caching for repeated queries
        - Parallel tool execution when possible
        - Cost optimization strategies
    