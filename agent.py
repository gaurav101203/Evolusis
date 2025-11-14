"""
Core agent: receives query, decides which tool to call,
and composes reasoning and final answer using Gemini as the LLM.
"""

import os
import asyncio
from utils.decision import needs_weather, needs_news
from external_tools.weather import get_weather
from external_tools.news import get_news_headlines
from utils.memory import ShortTermMemory
import google.generativeai as genai

# Configure Gemini client from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment (.env)")

genai.configure(api_key=GEMINI_API_KEY)

# simple memory (optional)
memory = ShortTermMemory(max_items=5)

async def call_gemini_system(prompt: str, temperature: float = 0.2) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    if isinstance(response, str):
        return response
    if hasattr(response, "text"):
        return response.text
    # fallback: return repr
    return str(response)

async def handle_query(query: str):
    memory.add(query)

    reasoning_parts = []
    answer = None

    if needs_weather(query):
        reasoning_parts.append("Detected weather intent → calling OpenWeatherMap.")
        weather = get_weather(query)
        prompt = f"""User asked: "{query}"
I fetched weather facts:
- city: {weather.get('city')}
- temp: {weather.get('temp')}°C
- desc: {weather.get('desc')}
Write a concise user-facing answer (one or two sentences) that includes the temperature and conditions."""
        answer = await call_gemini_system(prompt)
    elif needs_news(query):
        reasoning_parts.append("Detected news intent → calling News API.")
        headlines = get_news_headlines(query, max_articles=3)
        prompt = f"""User asked: "{query}"
I fetched these headlines and summaries:
{headlines}

Summarize the most relevant points in 2-3 sentences."""
        answer = await call_gemini_system(prompt)
    else:
        reasoning_parts.append("General question → letting Gemini answer directly.")
        mem_items = memory.get_all()
        mem_text = "\n".join(f"- {m}" for m in mem_items[-3:]) if mem_items else ""
        prompt = f"""You are an assistant. Answer the user's question concisely.

Recent user queries:
{mem_text}

Question: {query}
Answer:"""
        answer = await call_gemini_system(prompt)

    reasoning = " ".join(reasoning_parts)
    return {"reasoning": reasoning, "answer": answer or "Sorry, could not generate an answer."}
