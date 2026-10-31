from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "wetter"
titel = "Wetter (Open-Meteo)"
kategorie = "Alltag"
beschreibung = "Wetter für jeden Ort, ohne Schlüssel."
kosten = GRATIS
env = []
key_url = "https://open-meteo.com"


def test():
    return http_test("https://api.open-meteo.com/v1/forecast", params={"latitude": 52.52, "longitude": 13.41, "current": "temperature_2m"})
