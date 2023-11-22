import asyncio
from pathlib import Path
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel_issue.helpers import (
    chat_config_dict,
    create_semantic_function_chat_config,
)

GREEN_COLOR = "\033[32m"
RED_COLOR = "\033[31m"
RESET_COLOR = "\033[0m"

RAG_PROMPT = Path(__file__).with_name("prompt.txt").read_text()


def get_prompt(query: str):
    return f"""
{RAG_PROMPT}

QUESTION
------------
{query}
"""


class ChatService:
    def __init__(self, azure_endpoint: str, azure_api_key: str) -> None:
        self._kernel = sk.Kernel()
        self._kernel.add_chat_service(
            "azure_gpt4",
            AzureChatCompletion(
                "gpt-4",
                azure_endpoint,
                azure_api_key,
            ),
        )
        self._kernel.set_default_chat_service("azure_gpt4")
        self._chat = self._kernel.register_semantic_function(
            skill_name="Chatbot",
            function_name="chat",
            function_config=create_semantic_function_chat_config(
                "{{$input}}",
                chat_config_dict,
                self._kernel,
            ),
        )

    async def chat(self, prompt: str):
        result = await self._kernel.run_async(self._chat, input_str=prompt)
        return result


async def main():
    _deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    chat_service = ChatService(azure_endpoint=endpoint, azure_api_key=api_key)

    while True:
        print(f"{GREEN_COLOR}(Your turn) Please enter your prompt:{RESET_COLOR}")
        query = input()
        # doesn't fail if I create a new service at each iteration
        # chat_service = ChatService(azure_endpoint="...", azure_api_key="api key")
        prompt = get_prompt(query)
        output = await chat_service.chat(prompt)
        print(f"{GREEN_COLOR}(LLM) Response:{RESET_COLOR}")
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
