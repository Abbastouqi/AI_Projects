"""Fetch and summarize web research via SerpAPI to enrich chapter prompts."""
import httpx
from book_generator.core.config import get_settings
from book_generator.services.llm import chat_completion
from book_generator.core.logger import logger


def search_articles(query: str, num: int = 3) -> list[dict]:
    """Return top N search results from SerpAPI."""
    key = get_settings().serpapi_key
    if not key:
        logger.warning("SERPAPI_KEY not set — skipping research")
        return []
    params = {"q": query, "api_key": key, "num": num, "engine": "google"}
    try:
        resp = httpx.get("https://serpapi.com/search", params=params, timeout=15)
        resp.raise_for_status()
        results = resp.json().get("organic_results", [])[:num]
        return [{"title": r.get("title"), "snippet": r.get("snippet"), "link": r.get("link")} for r in results]
    except Exception as e:
        logger.error(f"SerpAPI error: {e}")
        return []


def summarize_article(snippet: str, title: str) -> str:
    prompt = f"Summarize the following article snippet in 2-3 sentences for use as research context in a book chapter.\nTitle: {title}\nSnippet: {snippet}"
    return chat_completion(prompt, temperature=0.3)


def get_research_context(chapter_title: str, book_title: str) -> str:
    """Fetch top articles and return a summarized research block string."""
    query = f"{book_title} {chapter_title}"
    articles = search_articles(query)
    if not articles:
        return ""
    summaries = []
    for a in articles:
        summary = summarize_article(a.get("snippet", ""), a.get("title", ""))
        summaries.append(f"- [{a['title']}]({a['link']}): {summary}")
    block = "\n".join(summaries)
    logger.info(f"Research context built for chapter: {chapter_title}")
    return block
