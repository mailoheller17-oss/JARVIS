from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "elevenlabs"
titel = "ElevenLabs"
kategorie = "Sprache"
beschreibung = "Natürliche Stimme für Jarvis (Gratis-Kontingent ~10k Zeichen/Monat)."
kosten = KONTINGENT
env = ['ELEVENLABS_API_KEY']
key_url = "https://elevenlabs.io/app/settings/api-keys"
voice_id = _env("ELEVENLABS_VOICE_ID") or "onwK4e9ZLuTAKqWW03F9"  # "Daniel", ruhige Stimme, multilingual


def test():
    return http_test("https://api.elevenlabs.io/v1/user", headers={"xi-api-key": _env("ELEVENLABS_API_KEY")})
