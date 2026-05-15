1) LEGEND:
    developer <- person who will interact with development agent.
    development agent <- agent which will help developer to create other agents.
    User <- person who will interact with the main agent.
    main_agent <- main agent which will be able to interact with the custom agents, it will classify the query and assign corresponding custom agent to it.
    custom_agent <- agent which will be created by the development agent and will be instructed to do given task in the domain it specializes.
    MCP_SERVER_dataclass <- dataclass for the mcp server which will be passed to the custom agents so they will be capable to use it.
    TOOL_DATACLASS <- dataclass for the custom agent which will be passed to the custom agents so they will be capable to use it.
    SKILL_DATACLASS <- dataclass for skills that contain reusable knowledge/instructions.
    AGENT_DATACLASS <- dataclass for agent metadata used in agent registry.
    RESPONSE_DATACLASS <- dataclass for standardized responses between agents.


2) Development
    
    2.1) IDEA:

        I want to build the system where a developer and develpment agent can interact in order to create custom agents tooling/skills/mcp_servers assosieted with particular agetns. These custom agents will be able to interact with the mcp server and use the tools provided by the mcp server and call other custom agents when they notice that particular task falls under their domain. 

    2.2) PATHS:

        MCP_SERVERS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\mcp_servers
        CUSTOM_AGENTS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\custom_agents
        SKILLS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\skills
        TOOLS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\tools
        CONFIG_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\config

    2.3) Implemenation:
        
        2.3.1) Specification: Understanding the domain and required specification. -- \agents\development\Specification.md
            
            touch CUSTOM_AGENTS_PATH/<custom_agent_name>/specification.md

            Write the document which will instruct the development agent to demand the answers for the developer about the domain and required specification of the custom agent. It should answer the questions like:
                """
                2.3.1.1) Basic understanding:
                    What is the domain of the custom agent?
                    What are possible use cases of the custom agent?
                    .............................................
                
                Append the basic understanding of the custom agent in the specification.md file.
                
                2.3.1.2) Required specification:
                    What is the required specification of the custom agent?
                    What is the required specification of the mcp server?
                    What is the required specification of the tools?
                    What is the required specification of the skills?
                    What is the required specification of the custom agent?
                
                2.3.1.3) Check if any of the required skills/tools/mcp_servers are already available?
                    If yes, then provide the link to the available skill/tool/mcp_server and ask the developer whether it matches the requirements.
                    If no, then add to the specification that such thing needs to be created.
                
                2.3.1.4) Dependency validation:
                    Check for circular dependencies between subagents.
                    Validate that all required tools/MCP servers are available.
                    Ensure subagent capabilities match the requirements.

                Append the basic understanding of the custom agent in the specification.md file.
                """

        2.3.2) MCP Server creation module -- agents\development\mcp_creation.md
            
            Write a document which will guide the development agent how to create mcp server with the help of the developer. It should contain:
                 MCP Server creation module
                 MCP tool creation module
                 MCP tool description - openai_standard module
                 MCP server connection handling and error recovery

            Write a McpServerDataclass which could be passed to the custom agent, it should contain all the required information in order to communicate with mcp server, extract its tools with definitions:
                - server_name: str
                - server_path: str
                - connection_config: dict
                - tools: list[ToolDataclass]
                - health_check_endpoint: str (optional)
                - timeout: int (default: 30)

        2.3.3) Tool creation module -- agents\development\tool_creation.md

            Write a document which will guide the development agent how to create tool with the help of the developer. It should contain:
                Tool format openai_standard
                Tool creation module
                Tool description module
                Tool validation and testing
                Submit tool creation module <- Specific and required type of tool which will validate and capture the llm response which allow python communication between the custom agents
            
            Write a ToolDataclass which could be passed to the custom agent, it should contain all the required information in order to communicate with tool function, extract its definitions:
                - tool_name: str
                - tool_path: str
                - function_reference: callable
                - openai_schema: dict
                - validation_schema: dict (optional)
                - error_handling: dict (optional)

            **hard** Write a special submit tool which will be used to submit the llm response and validate it and pass it to the caller. This tool should:
                - Validate response format
                - Handle errors gracefully
                - Support retry logic
                - Return standardized ResponseDataclass

        2.3.4) Skill creation module -- agents\development\skill_creation.md

            Write a document which will guide the development agent how to create skill with the help of the developer. It should contain the skill itself but also it should prepare short description of the skill.

            Write a SkillDataclass which could be passed to the custom agent, it should contain all the required information in order to extract the skill body and short definition:
                - skill_name: str
                - skill_path: str
                - short_description: str (max 200 chars)
                - full_instruction: str
                - usage_examples: list[str] (optional)
                - related_tools: list[str] (optional)
    
        2.3.5) Custom prompt creation module -- agents\development\prompt_creation.md

            Write a document which will guide the development agent how to create custom prompts with the help of the developer. It should contain:
                - Prompt structure and best practices
                - Domain-specific instructions
                - Tool usage guidelines
                - Error handling instructions
                - Examples of good prompts

        2.3.6) Custom agent creation module -- agents\development\agent_creation.md

            Write basic agent creation instruction which will instruct the developer agent how to create custom agent. Newly created custom agent class will implement abstract class CustomAgent and should accept tools, mcp servers, skill paths, custom prompt, possible subagents as the init argument. This class will create the agent in the C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\custom_agents folder. And will add this custom agent to the agent_registry.json file, with description and list of available tools, mcp servers and skills for this agent, it will also contain the list of subagents it can call.
        
            class <agent_name>(CustomAgent):
                def __init__(self,
                    agent_name: str,  # max_len=100
                    short_agent_description: str,  # min_len=100, max_len=1000
                    mcp_servers: list[MCPServerDataClass],
                    tools: list[ToolDataclass],
                    skills: list[SkillDataClass],
                    subagents: list[AgentDataClass],
                    custom_prompt: str,
                    max_subagent_depth: int = 3,  # Prevent infinite recursion
                ):
                    super().__init__()
                    # Initialize agent with validation
                    self._validate_dependencies()
                    self._register_agent()

                def run(self, query: str|dict, depth: int = 0) -> ResponseDataclass:
                    """
                    Execute agent with query.
                    Args:
                        query: User query (string or structured dict)
                        depth: Current recursion depth for subagent calls
                    Returns:
                        ResponseDataclass with standardized response
                    """
                    if depth > self.max_subagent_depth:
                        raise RecursionError("Max subagent depth exceeded")
                    
                    # Process query and return response
                    pass
                
                def _validate_dependencies(self) -> bool:
                    """Validate all tools, MCP servers, and subagents are available"""
                    pass
                
                def _register_agent(self) -> None:
                    """Register agent in agent_registry.json"""
                    pass
            


3) Using

    3.1) IDEA:

        I want to create main agent which will interact with the user. User sends the query and main agent will send the query to the appropriate subagents. Custom agent will return the results and main agent will return the results to the user. Custom agent can delegate further the task into the subagents.
    
    3.2) Paths:

        AGENT_REGISTRY_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\config\agent_registry.json
        MAIN_AGENT_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\src\main_agent
        LOGS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\logs (optional for future logging)

    3.3) Implementation:

        3.3.1) Agent Registry:
            Create agent_registry.json that stores:
                - agent_name
                - agent_description
                - capabilities (list of domains/tasks)
                - available_tools
                - available_mcp_servers
                - available_skills
                - subagents
                - version
                - status (active/inactive)

        3.3.2) Main Agent:
            Create MainAgent class that:
                - Loads agent registry
                - Routes queries to appropriate custom agents
                - Handles agent responses
                - Manages error handling and retries
                - Returns final response to user
            
            class MainAgent:
                def __init__(self):
                    self.agent_registry = self._load_registry()
                    self.active_agents = self._initialize_agents()
                
                def process_query(self, query: str) -> ResponseDataclass:
                    """
                    Main entry point for user queries.
                    1. Analyze query
                    2. Select appropriate agent(s)
                    3. Execute agent(s)
                    4. Aggregate results
                    5. Return response
                    """
                    pass
                
                def _route_query(self, query: str) -> AgentDataClass:
                    """Determine which agent should handle the query"""
                    pass
                
                def _execute_agent(self, agent: AgentDataClass, query: str) -> ResponseDataclass:
                    """Execute selected agent with error handling"""
                    pass

        3.3.3) Response Format:
            All agents return ResponseDataclass:
                - status: "success" | "error" | "partial"
                - data: dict (actual response data)
                - metadata: dict (execution info, tokens used, etc.)
                - errors: list[dict] | None
                - agent_chain: list[str] (track which agents were called)

        3.3.4) Error Handling:
            - Agent not found: fallback to general agent or return error
            - Agent execution failure: retry with exponential backoff
            - Timeout: return partial results if available
            - Circular dependency: detect and prevent with depth tracking

        3.3.5) Communication Protocol:
            Agents communicate via:
                - Direct function calls (same process)
                - Standardized ResponseDataclass format
                - Query validation before execution
                - Result validation after execution

4) Future Enhancements (Optional):

    4.1) Monitoring & Observability:
        - Structured logging can be added
        - Metrics collection (latency, success rate, cost)
        - Tracing for multi-agent calls

    4.2) Performance Optimization:
        - Caching frequently used results
        - Rate limiting for API calls
        - Load balancing for multiple agent instances

    4.3) Advanced Features:
        - Agent versioning and rollback
        - A/B testing different agent configurations
        - Hot-reload for agent updates
        - Web UI for agent management



 