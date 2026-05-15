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

    2.3)SIMPLIFIED PLAN:
        2.3.0) Create directory for cutom agent.
            
            mkdir CUSOTM_AGENTS_PATH/<custom_agent_name>
        
        2.3.1) Specification: Understanting the domain and required specification of the custom agent.
            
            touch CUSOTM_AGENTS_PATH/<custom_agent_name>/specification.md

            Write the document which will describe the domain and required specification of the custom agent. It shoudl anser the questions like:
                
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
                
                Append the basic understanding of the custom agent in the specification.md file.

        2.3.2) MCP Server creation module
            
            Write basic mcp server creatin instruction which will help development agent to create mcp servers with the help of the developer. It shoud contain:
                 MCP Server creation module/ 
        
        2.3.3) Tool creation module
        2.3.4) Skill creation module
        2.3.5) Custom prompt creation module
        2.3.6) Custom agent creation module

            Wirte basic agent creation class which will accept the tool's, and mcp servers, skill paths and custom prompt as the init argument. This class will create the agent in in the C:\Users\mgodl\Downloads\bob_hackaton\agents\custom_agents folder. And will add this custom agent to the agents_list.json file, with descriton and list of available tools, mcp servers and skills for this agents, it will also contain the list of subagents it can call.

        Custom agent creatin class
            init ()
            add/remove(mcp_server)
            add/remove(tool)
            add/remove(skill)
            add/remove(subagent)
            add/remove(prompt)
            add/remove(description)
            create_agent_directory() <- requres at least the prompt and one (tool or mcp) to to be added
                create_agent_file() <- called automaticly by the create_agent_directory() function.


3) Using



 