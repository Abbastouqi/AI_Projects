"""OpenAI LLM service with retry logic."""
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI, RateLimitError, APIError
from book_generator.core.config import get_settings
from book_generator.core.logger import logger

_client: OpenAI | None = None


def get_llm() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=get_settings().openai_api_key)
    return _client


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=4, max=30),
    reraise=True,
)
def chat_completion(prompt: str, temperature: float = 0.7) -> str:
    """Send a prompt and return the raw text response."""
    settings = get_settings()
    logger.debug(f"LLM call | model={settings.openai_model} | prompt_len={len(prompt)}")
    response = get_llm().chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    text = response.choices[0].message.content.strip()
    logger.debug(f"LLM response_len={len(text)}")
    return text


def chat_json(prompt: str, temperature: float = 0.7) -> dict:
    """Call LLM and parse JSON response. Raises ValueError on bad JSON."""
    raw = chat_completion(prompt, temperature)
    # Strip markdown fences if model adds them despite instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}\nRaw: {raw[:500]}")
        raise ValueError(f"LLM returned invalid JSON: {e}") from e
