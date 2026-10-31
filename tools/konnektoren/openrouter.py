from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "openrouter"
titel = "OpenRouter"
kategorie = "KI-Text"
beschreibung = "Viele Modelle, einige mit :free komplett gratis."
kosten = KONTINGENT
env = ["OPENROUTER_API_KEY"]
key_url = "https://openrouter.ai/keys"
llm = {
    "base_url": "https://openrouter.ai/api/v1",
    "model": _env("OPENROUTER_MODEL") or "meta-llama/llama-3.3-70b-instruct:free",
    "key_env": "OPENROUTER_API_KEY",
    "prioritaet": 40,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
