"""DeepSeek OpenAI-compatible LLM backend."""

from __future__ import annotations

from libs.llm.openai_llm import OpenAICompatibleLLM


class DeepSeekLLM(OpenAICompatibleLLM):
    """DeepSeek chat completion backend."""

    provider_name = "deepseek"
    default_base_url = "https://api.deepseek.com/v1"
    api_key_env_name = "DEEPSEEK_API_KEY"
    default_model = "deepseek-chat"
