from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "groq"
titel = "Groq"
kategorie = "KI-Text"
beschreibung = "Blitzschnelle Open-Source-Modelle (Llama)."
kosten = KONTINGENT
env = ["GROQ_API_KEY"]
key_url = "https://console.groq.com/keys"
llm = {
    "base_url": "https://api.groq.com/openai/v1",
    "model": _env("GROQ_MODEL") or "llama-3.3-70b-versatile",
    "key_env": "GROQ_API_KEY",
    "prioritaet": 20,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
