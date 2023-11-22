from semantic_kernel import (
    ChatPromptTemplate,
    PromptTemplateConfig,
    SemanticFunctionConfig,
)


def create_semantic_function_chat_config(prompt_template, prompt_config_dict, kernel):
    chat_system_message = (
        prompt_config_dict.pop("system_prompt")
        if "system_prompt" in prompt_config_dict
        else None
    )

    prompt_template_config = PromptTemplateConfig.from_dict(prompt_config_dict)

    prompt_template = ChatPromptTemplate(
        template=prompt_template,
        prompt_config=prompt_template_config,
        template_engine=kernel.prompt_template_engine,
    )

    if chat_system_message is not None:
        prompt_template.add_system_message(chat_system_message)

    return SemanticFunctionConfig(prompt_template_config, prompt_template)


chat_config_dict = {
    "schema": 1,
    # The type of prompt
    "type": "completion",
    # A description of what the semantic function does
    "description": "A chatbot which provides information about anything",
    # # Specifies which model service(s) to use
    # "default_services": [],
    # The parameters that will be passed to the connector and model service
    "completion": {
        "temperature": 0.0,
        "top_p": 1,
        "max_tokens": 500,
        "number_of_responses": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    },
    # Defines the variables that are used inside of the prompt
    "input": {
        "parameters": [
            {
                "name": "input",
                "description": "The input given by the user",
                "defaultValue": "",
            },
        ]
    },
    # Non-schema variable
    "system_prompt": (
        "You are a chatbot to provide information about anything you know. "
        "For other questions not related to places, you should politely decline to "
        "answer the question, stating your purpose"
    ),
}
