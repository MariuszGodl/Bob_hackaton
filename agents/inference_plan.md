
1) Inference module

    Create inference module which will accept the query, list[ToolDataclass] ,list[McpDataclass], list[SkillDataclass] as input. It needs to convert all the tools includeing the mcp tools into the openai tool standard and then use the openai api to generate the response.
    Whole skills should not be put in the query but only short descriptin of the skills should be included. That means if the llm will need to use the instrucitons provied in the skills it will need to call the tool which will return the whole instruction.

2) Custom agenet class

    Custom agent class should be abstraction of the custom agent it should expose the methods to interact with the inference module.
    