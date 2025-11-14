import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not set")

def _extract_city(query: str) -> str:
    m = re.search(r"in\s+([A-Za-z\s\-]+)", query, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return query.split()[-1].strip().strip("?")

def get_weather(query: str):
    city = _extract_city(query)
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return {"city": city, "temp": temp, "desc": desc}
