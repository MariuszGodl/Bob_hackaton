1) LEGEND:
    developer <- person who will interact with development agent to create custom agents.
    development agent <- agent which will help developer to create other agents.
    User <- person who will interact with the main agent.
    main_agent <- main agent which will classify the query and assign corresponding custom agent to it.
    custom_agent <- agent which will be created by the development agent and will be instructed to do given task in the domain it specializes.

2) DEVELOPER WORKFLOW (Creating Custom Agents)

    2.1) High-Level Process:
        
        Developer → Development Agent → Create Custom Agent → Register in System
        
    2.2) Steps:
        
        Step 1: Specification
            - Developer describes the domain and requirements
            - Development agent asks clarifying questions
            - Document is created with agent specification
        
        Step 2: Resource Creation
            - Create/select MCP servers
            - Create/select tools
            - Create/select skills
            - Define custom prompt
        
        Step 3: Agent Assembly
            - Development agent creates custom agent class
            - Validates dependencies
            - Registers agent in system
        
        Step 4: Testing
            - Developer tests the custom agent
            - Iterates if needed

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
        
        Development Side:
            - Development Agent (helps create custom agents)
            - Agent Builder (creates agent files and configuration)
            - Agent Registry (stores agent metadata)
        
        Runtime Side:
            - Main Agent (entry point for users)
            - Custom Agents (specialized agents for specific domains)
            - Tools, MCP Servers, Skills (resources used by agents)
    
    4.2) Key Principles:
        
        - Modular: Each agent is independent
        - Hierarchical: Agents can call subagents
        - Validated: Dependencies are checked before creation
        - Standardized: All agents use same communication format
        - Safe: Depth limits prevent infinite loops
