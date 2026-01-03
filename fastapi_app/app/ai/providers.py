# fastapi_app/app/ai/providers.py

from abc import ABC, abstractmethod

from openai import OpenAI


class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        raise NotImplementedError


class OpenAIProvider:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.2,
    ) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # lub gpt-4o / gpt-3.5-turbo
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional meteorologist.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content.strip()


def get_provider(name: str, api_key: str):
    if name == "openai":
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing")
        return OpenAIProvider(api_key)

    raise RuntimeError(f"Unknown AI provider: {name}")
