from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "sambanova"
titel = "SambaNova"
kategorie = "KI-Text"
beschreibung = "Schnelle Llama-Modelle mit Gratis-Kontingent."
kosten = KONTINGENT
env = ["SAMBANOVA_API_KEY"]
key_url = "https://cloud.sambanova.ai/apis"
llm = {
    "base_url": "https://api.sambanova.ai/v1",
    "model": _env("SAMBANOVA_MODEL") or "Meta-Llama-3.3-70B-Instruct",
    "key_env": "SAMBANOVA_API_KEY",
    "prioritaet": 60,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
