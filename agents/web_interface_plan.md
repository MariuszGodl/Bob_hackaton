# Web Interface Plan - Universal Visual Workflow Designer

## 1) OVERVIEW

    1.1) Purpose:
        Create a universal web-based interface where users can visually design, document, and modify ANY type of workflow through conversation with the main agent. The interface displays diagrams showing how different modules/components connect with each other, with expandable notes for detailed documentation.

    1.2) Supported Workflow Types:
        - Agent workflows (multi-agent systems)
        - Database schemas (tables, relationships, constraints)
        - Data flow diagrams (ETL pipelines, data transformations)
        - System architecture (microservices, APIs, infrastructure)
        - Business processes (BPMN-style workflows)
        - API integrations (endpoints, data flow)
        - Software architecture (modules, dependencies)
        - Network topology (servers, connections, protocols)
        - CI/CD pipelines (stages, dependencies, triggers)
        - And any other modular system

    1.3) Key Features:
        - Universal graph/diagram visualization
        - Conversational interface with main agent
        - Click-to-expand notes on each component
        - Real-time workflow modification
        - Multi-format document generation
        - Template library for common workflows
        - Export to various diagram formats

## 2) ARCHITECTURE

    2.1) Core Components:
        
        Frontend:
            - React/Vue.js web application
            - Universal graph visualization (React Flow)
            - Multi-mode diagram renderer
            - Chat interface component
            - Notes panel with rich text editor
            - Template selector
            - Multi-format export engine
        
        Backend:
            - Main Agent API (conversational interface)
            - Workflow state management
            - Template library
            - Document generation service
            - Diagram export service (SVG, PNG, PDF)
        
        Storage:
            - Workflow definitions (JSON)
            - Notes database
            - Template library
            - User preferences

    2.2) User Flow:
        
        User → Select Workflow Type → Chat with Main Agent → Build Diagram → Add Notes → Export Documentation

## 3) UNIVERSAL GRAPH SYSTEM

    3.1) Node Types (Configurable per Workflow):
        
        Agent Workflows:
            - Agent nodes
            - Tool nodes
            - MCP Server nodes
            - Skill nodes
        
        Database Schema:
            - Table nodes
            - View nodes
            - Stored procedure nodes
            - Trigger nodes
        
        Data Flow:
            - Data source nodes
            - Transformation nodes
            - Destination nodes
            - Processing nodes
        
        System Architecture:
            - Service nodes
            - Database nodes
            - API Gateway nodes
            - Load Balancer nodes
            - Cache nodes
        
        Business Process:
            - Task nodes
            - Decision nodes
            - Event nodes
            - Gateway nodes
        
        Custom:
            - User-defined node types
            - Configurable properties
            - Custom styling

    3.2) Edge Types (Configurable per Workflow):
        
        Agent Workflows:
            - Delegation (agent → subagent)
            - Tool usage (agent → tool)
            - Data flow (agent → agent)
        
        Database Schema:
            - Foreign key (table → table)
            - One-to-many relationship
            - Many-to-many relationship
        
        Data Flow:
            - Data pipeline (source → transformation → destination)
            - Conditional flow
            - Parallel processing
        
        System Architecture:
            - HTTP/REST calls
            - Message queue
            - Database connection
            - gRPC
        
        Business Process:
            - Sequence flow
            - Conditional flow
            - Message flow
        
        Custom:
            - User-defined edge types
            - Configurable labels
            - Custom styling

    3.3) Visual Representation:
        
        Layout Options:
            - Hierarchical (top-down, left-right)
            - Force-directed (organic)
            - Circular
            - Grid
            - Custom positioning
        
        Node Styling:
            - Shape (rectangle, circle, diamond, custom)
            - Color (by type, status, custom)
            - Size (by importance, data volume, custom)
            - Icons (type-specific)
            - Badges (status indicators)
        
        Edge Styling:
            - Line type (solid, dashed, dotted)
            - Arrow type (single, double, none)
            - Color (by type, status)
            - Labels (relationship type, data type)
            - Thickness (by importance, data volume)

## 4) WORKFLOW MODES

    4.1) Mode Selection:
        
        On startup or via menu:
            - "What type of workflow do you want to create?"
            - Display template gallery
            - User selects or describes custom workflow
        
        Mode determines:
            - Available node types
            - Available edge types
            - Default styling
            - Validation rules
            - Export format options

    4.2) Agent Workflow Mode:
        
        Focus: Multi-agent system design
        
        Node Types:
            - Main Agent
            - Custom Agents
            - Subagents
            - Tools
            - MCP Servers
            - Skills
        
        Connections:
            - Agent delegation
            - Tool usage
            - Resource access
        
        Notes:
            - Agent responsibilities
            - Tool descriptions
            - Integration points

    4.3) Database Schema Mode:
        
        Focus: Database design and documentation
        
        Node Types:
            - Tables (with columns)
            - Views
            - Stored Procedures
            - Triggers
            - Indexes
        
        Connections:
            - Foreign keys
            - Relationships (1:1, 1:N, N:M)
            - Dependencies
        
        Notes:
            - Column descriptions
            - Business rules
            - Constraints
            - Performance considerations
        
        Special Features:
            - Show/hide columns
            - Cardinality labels
            - Index visualization
            - SQL generation

    4.4) Data Flow Mode:
        
        Focus: ETL pipelines and data transformations
        
        Node Types:
            - Data Sources (databases, APIs, files)
            - Transformations (map, filter, aggregate)
            - Destinations (databases, data lakes, APIs)
            - Processing (batch, stream)
        
        Connections:
            - Data pipelines
            - Conditional flows
            - Error handling paths
        
        Notes:
            - Data formats
            - Transformation logic
            - Error handling
            - Performance metrics
        
        Special Features:
            - Data volume indicators
            - Processing time estimates
            - Error rate tracking

    4.5) System Architecture Mode:
        
        Focus: Microservices and infrastructure
        
        Node Types:
            - Services (REST, gRPC, GraphQL)
            - Databases (SQL, NoSQL)
            - Message Queues (Kafka, RabbitMQ)
            - Caches (Redis, Memcached)
            - Load Balancers
            - API Gateways
        
        Connections:
            - HTTP/REST calls
            - Message passing
            - Database connections
            - Cache access
        
        Notes:
            - Service responsibilities
            - API endpoints
            - Scaling strategies
            - Deployment info
        
        Special Features:
            - Technology stack labels
            - Port numbers
            - Protocol indicators
            - Health status

    4.6) Business Process Mode:
        
        Focus: BPMN-style business workflows
        
        Node Types:
            - Tasks (user, service, manual)
            - Events (start, end, intermediate)
            - Gateways (exclusive, parallel, inclusive)
            - Subprocesses
        
        Connections:
            - Sequence flow
            - Message flow
            - Association
        
        Notes:
            - Task descriptions
            - Decision criteria
            - SLA requirements
            - Responsible parties

    4.7) Custom Mode:
        
        Focus: User-defined workflows
        
        Features:
            - Define custom node types
            - Define custom edge types
            - Custom styling rules
            - Custom validation
            - Custom export formats

## 5) CONVERSATIONAL INTERFACE

    5.1) Universal Commands:
        
        Creation:
            - "Add a [node_type] called [name]"
            - "Create a [node_type] with [properties]"
            - "Insert [node_type] between [node1] and [node2]"
        
        Connection:
            - "Connect [node1] to [node2]"
            - "Add a [edge_type] from [node1] to [node2]"
            - "Remove connection between [node1] and [node2]"
        
        Modification:
            - "Change [node] to [new_properties]"
            - "Rename [node] to [new_name]"
            - "Update [node] description"
        
        Deletion:
            - "Remove [node]"
            - "Delete [node] and its connections"
        
        Organization:
            - "Group [nodes] into [group_name]"
            - "Rearrange layout"
            - "Auto-organize diagram"
        
        Documentation:
            - "Add note to [node]: [note_text]"
            - "Explain [node]"
            - "Document the connection between [node1] and [node2]"

    5.2) Mode-Specific Commands:
        
        Database Schema:
            - "Add column [name] to table [table]"
            - "Create foreign key from [table1].[column] to [table2].[column]"
            - "Add index on [table].[columns]"
        
        Data Flow:
            - "Add transformation: [logic]"
            - "Set data source to [source]"
            - "Configure error handling for [node]"
        
        System Architecture:
            - "Add REST endpoint [path] to [service]"
            - "Configure [service] to use [database]"
            - "Add load balancer for [services]"
        
        Agent Workflow:
            - "Make [agent] a subagent of [parent]"
            - "Give [agent] access to [tool]"
            - "Add [skill] to [agent]"

    5.3) Intelligent Suggestions:
        
        Main agent provides:
            - Best practices for current workflow type
            - Missing components detection
            - Optimization suggestions
            - Common patterns for the workflow type
            - Validation warnings

## 6) NOTES SYSTEM

    6.1) Universal Note Types:
        
        Component Notes:
            - Purpose and description
            - Technical specifications
            - Configuration details
            - Known issues
            - Future improvements
        
        Connection Notes:
            - Relationship description
            - Data format
            - Protocol details
            - Performance characteristics
        
        Group Notes:
            - Module overview
            - Design decisions
            - Dependencies
        
        Workflow Notes:
            - Overall architecture
            - Design patterns used
            - Trade-offs
            - Deployment considerations

    6.2) Note Interface:
        
        Adding Notes:
            - Click component → "Add Note" button
            - Via chat: "Add note to [component]: [text]"
            - Rich text editor with:
                - Markdown support
                - Code blocks
                - Tables
                - Links
                - Images
        
        Viewing Notes:
            - Hover: Show note indicator (icon with count)
            - Click: Expand panel with all notes
            - Toggle: Show/hide all notes on diagram
            - Search: Find notes by content
        
        Organizing Notes:
            - Tags (e.g., "important", "todo", "security")
            - Categories (by type, priority)
            - Timestamps (created, updated)
            - Author (if multi-user)

    6.3) Note Visibility Modes:
        
        Clean Mode (default):
            - Notes hidden
            - Small indicator on components with notes
            - Clean diagram view
        
        Overview Mode:
            - Show note titles only
            - Expandable on click
        
        Full Mode:
            - All notes visible
            - Useful for documentation review
        
        Presentation Mode:
            - Selected notes visible
            - Optimized for presentations

## 7) DOCUMENT GENERATION

    7.1) Export Formats:
        
        Diagram Formats:
            - SVG (scalable, editable)
            - PNG (high resolution)
            - PDF (printable)
            - Draw.io XML (editable in Draw.io)
            - Mermaid (text-based diagram)
        
        Documentation Formats:
            - Markdown (.md)
            - HTML (with embedded diagram)
            - PDF (complete documentation)
            - Confluence format
            - Notion format
            - JSON (workflow definition)

    7.2) Document Structure (Universal):
        
        1. Title and Overview
            - Workflow name
            - Type
            - Purpose
            - Last updated
        
        2. Visual Diagram
            - Embedded high-resolution image
            - Interactive HTML version (optional)
        
        3. Component Catalog
            - List all nodes with descriptions
            - Organized by type
            - Include properties
        
        4. Connections
            - List all relationships
            - Connection types
            - Data flow descriptions
        
        5. Notes Section
            - Organized by component
            - Expandable/collapsible
            - Searchable
            - Tagged and categorized
        
        6. Technical Details
            - Configuration
            - Dependencies
            - Version information
        
        7. Appendix
            - Glossary
            - References
            - Change log

    7.3) Mode-Specific Documentation:
        
        Database Schema:
            - DDL SQL scripts
            - Table definitions
            - Relationship matrix
            - Index recommendations
        
        Data Flow:
            - Pipeline configuration
            - Transformation logic
            - Data lineage
            - Performance metrics
        
        System Architecture:
            - Service catalog
            - API documentation
            - Deployment diagram
            - Infrastructure requirements
        
        Agent Workflow:
            - Agent specifications
            - Tool descriptions
            - Skill library
            - Routing logic

## 8) TEMPLATE LIBRARY

    8.1) Pre-built Templates:
        
        Agent Workflows:
            - Customer Support System
            - Data Analysis Pipeline
            - Content Moderation System
            - Research Assistant
        
        Database Schemas:
            - E-commerce Database
            - User Management System
            - Blog Platform
            - Inventory System
        
        Data Flows:
            - ETL Pipeline
            - Real-time Analytics
            - Data Warehouse Loading
            - API Integration
        
        System Architecture:
            - Microservices Architecture
            - Event-Driven System
            - CQRS Pattern
            - Serverless Architecture
        
        Business Processes:
            - Order Fulfillment
            - Employee Onboarding
            - Incident Management
            - Approval Workflow

    8.2) Template Features:
        
        Each template includes:
            - Pre-configured nodes and connections
            - Sample notes and documentation
            - Best practices built-in
            - Customization guide
            - Common variations
        
        User can:
            - Start from template
            - Modify via conversation
            - Save as new template
            - Share templates

