import os
import requests
from dotenv import load_dotenv
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise RuntimeError("NEWSAPI_KEY not set")

def get_news_headlines(query: str, max_articles: int = 3):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": max_articles,
        "sortBy": "relevancy",
        "apiKey": NEWSAPI_KEY,
        "language": "en"
    }
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    articles = data.get("articles", [])
    results = []
    for a in articles[:max_articles]:
        results.append({
            "title": a.get("title"),
            "source": a.get("source", {}).get("name"),
            "description": a.get("description")
        })
    if not results:
        return "No recent news found."
    # stringified summary for the Gemini prompt
    return "\n".join([f"- {r['title']} ({r['source']}): {r['description']}" for r in results])
