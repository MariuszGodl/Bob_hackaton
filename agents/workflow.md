1) LEGEND:
    developer <- person who will interact with development agent to create custom agents.
    development agent <- agent in Bob IDE (NOT a custom agent instance) that uses skills to help developer create custom agents.
    Bob IDE <- the IDE environment where the development agent runs.
    User <- person who will interact with the main agent.
    main_agent <- main agent which will classify the query and assign corresponding custom agent to it.
    custom_agent <- agent which will be created by the development agent and will be instructed to do given task in the domain it specializes.

2) DEVELOPER WORKFLOW (Creating Custom Agents with Bob IDE)

    2.1) High-Level Process:
        
        Developer → Bob IDE (Development Agent) → Create Custom Agent → Register in System
        
        NOTE: The development agent runs in Bob IDE and uses skills (instruction documents in agents/development/) to guide the developer through the creation process.
        
    2.2) Steps:
        
        Step 1: Specification (Bob uses Specification.md skill)
            - Developer describes the domain and requirements to Bob
            - Bob (using Specification skill) asks clarifying questions
            - Bob creates specification.md document with agent specification
        
        Step 2: Resource Creation (Bob uses creation skills)
            - Bob guides developer to create/select MCP servers (using mcp_creation.md skill)
            - Bob guides developer to create/select tools (using tool_creation.md skill)
            - Bob guides developer to create/select skills (using skill_creation.md skill)
            - Bob guides developer to define custom prompt (using prompt_creation.md skill)
        
        Step 3: Agent Assembly (Bob uses agent_creation.md skill)
            - Bob creates custom agent class file
            - Bob validates dependencies
            - Bob registers agent in agent_registry.json
        
        Step 4: Testing
            - Developer tests the custom agent
            - Iterates with Bob if needed
    
    2.3) Bob IDE Skills Location:
        
        All skills that guide Bob are located in:
        C:\Users\mgodl\Downloads\bob_hackaton\agents\development\
        
        These are instruction documents that Bob reads to know how to help the developer:
            - Specification.md (how to gather requirements)
            - mcp_creation.md (how to create MCP servers)
            - tool_creation.md (how to create tools)
            - skill_creation.md (how to create skills)
            - prompt_creation.md (how to create prompts)
            - agent_creation.md (how to assemble the final agent)

3) USER WORKFLOW (Using the System)

    3.1) High-Level Process:
        
        User → Main Agent → Custom Agent(s) → Response to User
        
    3.2) Steps:
        
        Step 1: User submits query
            - User sends natural language query to main agent
        
        Step 2: Query routing
            - Main agent analyzes the query
            - Selects appropriate custom agent(s)
        
        Step 3: Execution
            - Custom agent processes the query
            - Uses tools, MCP servers, and skills as needed
            - May delegate to subagents if required
        
        Step 4: Response
            - Results are aggregated
            - Main agent returns response to user

4) SYSTEM OVERVIEW

    4.1) Components:
        
        Development Side (Bob IDE):
            - Development Agent in Bob IDE (uses skills to help create custom agents)
            - Development Skills (instruction documents in agents/development/)
            - Agent Builder (creates agent files and configuration)
            - Agent Registry (stores agent metadata)
        
        Runtime Side (Production):
            - Main Agent (entry point for users)
            - Custom Agents (specialized agents for specific domains)
            - Tools, MCP Servers, Skills (resources used by agents)
    
    4.2) Key Principles:
        
        - Skill-Guided Development: Bob IDE uses skills to guide agent creation
        - Modular: Each agent is independent
        - Hierarchical: Agents can call subagents
        - Validated: Dependencies are checked before creation
        - Standardized: All agents use same communication format
        - Safe: Depth limits prevent infinite loops
    
    4.3) Important Distinction:
        
        Development Agent (Bob IDE):
            - Runs in Bob IDE environment
            - NOT a custom agent instance
            - Uses skills from agents/development/ folder
            - Helps developer create custom agents
        
        Custom Agents (Runtime):
            - Created by developer with Bob's help
            - Instances of CustomAgent class
            - Run in production to serve users
            - Use tools, MCP servers, and skills to perform tasks
