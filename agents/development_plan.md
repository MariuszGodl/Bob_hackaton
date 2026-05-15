1) LEGEND:
    developer <- person who will interact with development agent.
    development agent <- agent which will help developer to create other agents.
    User <- person who will interact with the main agent.
    main_agent <- main agent which will be able to interact with the custom agents, it will classyfy the query and assign corresponding custom agent to it.
    custom_agent <- agent which will be created by the development agent and will be instructed to do given task in the domain it specializes.
    MCP_SERVER_dataclass <- dataclass for the mcp server which will be passed to the custom agents so they will be capable to use it.
    TOOL_DATACLASS <- dataclass for the custom agent which will be passed to the custom agents so they will be capable to use it.


2) Development
    
    2.1) IDEA:

        I want to build the system where a developer and develpment agent can interact in order to create custom agents tooling/skills/mcp_servers assosieted with particular agetns. These custom agents will be able to interact with the mcp server and use the tools provided by the mcp server and call other custom agents when they notice that particular task falls under their domain. 

    2.2) PATHS:

        MCP_SERVERS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\mcp_servers
        CUSOTM_AGENTS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\custom_agents
        SKILLS_PATH = C:\Users\mgodl\Downloads\bob_hackaton\agents\usage\skills

    2.3) Implemenation:
        
        2.3.1) Specification: Understanting the domain and required specification. -- \agents\development\Specification.md
            
            touch CUSOTM_AGENTS_PATH/<custom_agent_name>/specification.md

            Write the document which will instruct the development agent to demand the answers for the developer about the domain and required specification of the custom agent. It shoudl anser the questions like:
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
                    If yes, then provide the link to the available skill/tool/mcp_server and ask the developer wethere it matches the requrements.
                    If no, then add to the specification that such think needs to be created.

                Append the basic understanding of the custom agent in the specification.md file.
                """

        2.3.2) MCP Server creation module -- agents\development\mcp_creation.md
            
            Write a document which will guide the development agent how to create mcp server with the help of the developer. It shoud contain:
                 MCP Server creation module
                 MCP tool creation module
                 MCP tool description - openai_standard module

            Write a McpServerDataclass which could be passed to the custom agent, it should contain all the required information in ordet to communicate with mcp server, extract its tools with defintions 

        2.3.3) Tool creation module -- agents\development\tool_creaton.md

            Write a document which will guide the development agent how to create tool with the help of the developer. It shoud contain:
                Tool format openai_standard
                Tool creation module
                Tool description module
                Submit tool creation module <- Specific and required type of tool which will validate and capture the llm resomense which allow python communication between the custom agents
            
            Write a ToolDataclass which could be passed to the custom agent, it should contain all the required information in order to communicate with tool funciton, extract its defintions.

            **hard** Write a special submit tool which will be used to submit the llm response and validate it and pass it to the caller.

        2.3.4) Skill creation module -- agents\development\skill_creation.md

            Write a document which will guide the development agent how to create skill with the help of the developer. It should contain the skill itself but also it shoudl prepare short descriptiion of the skill.

            Write a SkillDataclass which could be passed to the custom agent, it should contain all the required information in order to extract the skill body and short definition.
    
        2.3.5) Custom prompt creation module -- agents\development\prompt_creation.md

            Write a document which will guide the development agent how to create skill with the help of the developer. It should contain the skill itself but also it shoudl prepare short descriptiion of the skill.

        2.3.6) Custom agent creation module -- agents\development\agent_creation.md

            Wirte basic agent creation instruction which will instruct the developer agent how to create custom agent. Newly created cutom agetn class will implement abstract class custom agent and should  accept tool's, and mcp servers, skill paths, custom prompt, possible subagents as the init argument. This class will create the agent in in the C:\Users\mgodl\Downloads\bob_hackaton\agents\custom_agents folder. And will add this custom agent to the agents_list.json file, with descriton and list of available tools, mcp servers and skills for this agents, it will also contain the list of subagents it can call.
        
            class <agent_name> (Custom agent)
                init (self,
                    agent_name: str max_len=100, 
                    short_agent_description_min_len=100 max_len=1000,
                    mcp_servers: list[MCPServerDataClass],
                    tools: list[ToolDatacss],
                    skills: list[SkillDataClass],
                    subagents: list[AgentDataClass],
                )

                run(self, query: str|dict) -> dict[]:
            


3) Using

    3.1) IDEA:

        I want to create main agent which will interact wiht the user. User send's the query and main agent will send the query to the apropriate subagents. Customagent will return the results and main agent will return the results to the user. Custom agent can delegate further the task into the subagents.
    
    3.2) Paths:

    3.3



 