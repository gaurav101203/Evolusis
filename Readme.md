# Evolusis — Backend Developer Assignment (FastAPI + Google Gemini)

## Overview

This service demonstrates an LLM-backed agent that decides whether to:

- Call external APIs (OpenWeatherMap, Wikipedia, NewsAPI)
- Or answer directly using Google Gemini

It returns both the agent's **reasoning** and the **final answer** in JSON.

## Files

- `main.py` — FastAPI server with `/ask` endpoint.
- `agent.py` — Agent logic and Gemini integration.
- `external_tools/weather.py` — OpenWeatherMap integration.
- `external_tools/wikipedia.py` — MediaWiki API helper.
- `external_tools/news.py` — NewsAPI integration.
- `utils/decision.py` — Heuristics to choose tools.
- `utils/memory.py` — Optional short-term memory.
- `.env.example` — Environment variables example.

## Setup

1. Clone the repo.
2. Create a virtualenv and install requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-dotenv requests google-generativeai
```
