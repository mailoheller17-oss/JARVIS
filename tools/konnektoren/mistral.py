from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "mistral"
titel = "Mistral"
kategorie = "KI-Text"
beschreibung = "Europäische KI, Gratis-Stufe (Experiment-Plan)."
kosten = KONTINGENT
env = ["MISTRAL_API_KEY"]
key_url = "https://console.mistral.ai/api-keys"
llm = {
    "base_url": "https://api.mistral.ai/v1",
    "model": _env("MISTRAL_MODEL") or "mistral-small-latest",
    "key_env": "MISTRAL_API_KEY",
    "prioritaet": 50,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
