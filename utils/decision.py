import re

def needs_weather(query: str) -> bool:
    q = query.lower()
    if "weather" in q or re.search(r"\btemperature\b|\btemp\b|\brain\b|\bsunny\b|\bcloudy\b", q):
        return True
    return False

def needs_news(query: str) -> bool:
    q = query.lower()
    if "news" in q or "latest" in q or "today" in q:
        return True
    return False
