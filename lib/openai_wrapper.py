import os
import openai
from dotenv import load_dotenv


class OpenAiWrapper:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.chat = {}

    def complete_chat(self, prompt: str):
        self.chat = openai.ChatCompletion.create(model=self.model, messages=prompt)

    def get_first_message(self):
        return self.chat.get("choices")[0].get("message").get("content")
