import json

from openai import OpenAI

from prompter import Prompter


class OpenAIPrompter(Prompter):
    def __init__(self):
        super().__init__("gpt-4o-2024-11-20")
        json_text = json.load(open('credentials.json'))
        self.client = OpenAI(
            api_key=json_text["api_key"],
        )

    def prompt_model(self, system_msg: str, question: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": question},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content
