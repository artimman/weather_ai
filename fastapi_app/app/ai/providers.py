# fastapi_app/app/ai/providers.py

import os
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        raise NotImplementedError

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str):
        import openai
        openai.api_key = api_key
        self.client = openai

    def generate(self, prompt: str, **kwargs):
        # synchronous example; production should be async and streaming-capable
        resp = self.client.Completion.create(
            engine=kwargs.get("engine", "text-davinci-003"),
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 500),
            temperature=kwargs.get("temperature", 0.2),
        )
        return resp["choices"][0]["text"].strip()

def get_provider(name: str, api_key: str):
    if name == "openai":
        return OpenAIProvider(api_key)
    # add Groq/Gemini implementations similarly
    raise ValueError("Unknown provider")


# TODO!

# class NoAIProvider(BaseProvider):
#     def generate(self, prompt: str, **kwargs):
#         raise RuntimeError("AI provider disabled")


# def get_provider(name: str, api_key: str):
#     if name in ("none", "", None):
#         return NoAIProvider()

#     if name == "openai":
#         from .openai_provider import OpenAIProvider
#         return OpenAIProvider(api_key)

#     raise ValueError("Unknown provider")
