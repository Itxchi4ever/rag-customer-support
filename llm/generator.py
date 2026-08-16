import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


class HuggingFaceGenerator:
    def __init__(self):
        token = os.getenv("HF_TOKEN")

        if not token:
            raise ValueError(
                "HF_TOKEN not found in environment variables."
            )

        self.client = InferenceClient(
            api_key=token
        )

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content