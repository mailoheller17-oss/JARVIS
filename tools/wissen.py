"""Live-Wissen für den Chat: Wetter, Wikipedia, Trends. Alles ohne Schlüssel."""
import os
import re
import xml.etree.ElementTree as ET

import httpx

UA = {"User-Agent": "JarvisApp/1.0 (https://github.com/mailoheller17-oss/JARVIS; persoenlicher Assistent)"}
WMO = {0: "klar", 1: "meist klar", 2: "teils bewölkt", 3: "bedeckt", 45: "Nebel", 48: "Nebel", 51: "Niesel",
       53: "Niesel", 55: "Niesel", 61: "leichter Regen", 63: "Regen", 65: "starker Regen", 71: "Schnee",
       73: "Schnee", 75: "viel Schnee", 80: "Schauer", 81: "Schauer", 82: "heftige Schauer", 95: "Gewitter"}


async def wetter(c: httpx.AsyncClient, text: str) -> str | None:
    m = re.search(r"wetter\w*\s+(?:in|für|fuer|bei)\s+([A-Za-zÄÖÜäöüß\- ]+)", text, re.I)
    ort = (m.group(1).strip() if m else os.environ.get("JARVIS_ORT", "Berlin")).split(" morgen")[0]
    g = (await c.get("https://geocoding-api.open-meteo.com/v1/search",
                     params={"name": ort, "count": 1, "language": "de"})).json()
    if not g.get("results"):
        return None
    r = g["results"][0]
    w = (await c.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": r["latitude"], "longitude": r["longitude"], "timezone": "auto", "forecast_days": 2,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code"})).json()
    cur, d = w["current"], w["daily"]
    return (f"Wetter {r['name']}: jetzt {cur['temperature_2m']}°C, {WMO.get(cur['weather_code'], '?')}, "
            f"Wind {cur['wind_speed_10m']} km/h. Heute {d['temperature_2m_min'][0]}–{d['temperature_2m_max'][0]}°C, "
            f"Regen {d['precipitation_probability_max'][0]}%. Morgen {d['temperature_2m_min'][1]}–"
            f"{d['temperature_2m_max'][1]}°C, {WMO.get(d['weather_code'][1], '?')}, Regen {d['precipitation_probability_max'][1]}%.")


async def wiki(c: httpx.AsyncClient, text: str) -> str | None:
    m = re.search(r"(?:was ist|was sind|wer ist|wer war|erklär\w* (?:mir )?|erklaer\w* (?:mir )?)(?:ein |eine |der |die |das )?(.+)", text, re.I)
    if not m:
        return None
    q = m.group(1).strip(" ?!.")[:80]
    s = (await c.get("https://de.wikipedia.org/w/api.php", headers=UA, params={
        "action": "opensearch", "search": q, "limit": 1, "format": "json"})).json()
    if not s[1]:
        return None
    r = await c.get("https://de.wikipedia.org/api/rest_v1/page/summary/" + s[1][0].replace(" ", "_"), headers=UA)
    if r.status_code != 200:
        return None
    return f"Wikipedia „{s[1][0]}“: {r.json().get('extract', '')[:700]}"


async def trends(c: httpx.AsyncClient, text: str) -> str | None:
    if not re.search(r"trend|viral|angesagt", text, re.I):
        return None
    r = await c.get("https://trends.google.com/trending/rss?geo=DE", headers=UA)
    titles = [i.findtext("title") for i in ET.fromstring(r.text).iter("item")][:10]
    return "Google-Trends Deutschland gerade: " + ", ".join(t for t in titles if t)


async def kontext(text: str) -> list[str]:
    out = []
    async with httpx.AsyncClient(timeout=8, follow_redirects=True) as c:
        for fn in (wetter, wiki, trends):
            if fn is wetter and not re.search(r"wetter|regen|temperatur|grad drau", text, re.I):
                continue
            try:
                r = await fn(c, text)
                if r:
                    out.append(r)
            except Exception:
                pass
    return out
