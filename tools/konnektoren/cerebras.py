from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "cerebras"
titel = "Cerebras"
kategorie = "KI-Text"
beschreibung = "Extrem schnelle Llama-Modelle, Gratis-Kontingent."
kosten = KONTINGENT
env = ["CEREBRAS_API_KEY"]
key_url = "https://cloud.cerebras.ai/"
llm = {
    "base_url": "https://api.cerebras.ai/v1",
    "model": _env("CEREBRAS_MODEL") or "llama-3.3-70b",
    "key_env": "CEREBRAS_API_KEY",
    "prioritaet": 30,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
