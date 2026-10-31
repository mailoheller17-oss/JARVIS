from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "gemini"
titel = "Gemini"
kategorie = "KI-Text"
beschreibung = "Googles KI, schnell und schlau. Großes Gratis-Kontingent."
kosten = KONTINGENT
env = ["GEMINI_API_KEY"]
key_url = "https://aistudio.google.com/apikey"
llm = {
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
    "model": _env("GEMINI_MODEL") or "gemini-2.5-flash",
    "key_env": "GEMINI_API_KEY",
    "prioritaet": 10,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
