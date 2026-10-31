from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "huggingface_text"
titel = "Hugging Face (Text)"
kategorie = "KI-Text"
beschreibung = "Open-Source-Modelle über den HF-Router."
kosten = KONTINGENT
env = ["HF_TOKEN"]
key_url = "https://huggingface.co/settings/tokens"
llm = {
    "base_url": "https://router.huggingface.co/v1",
    "model": _env("HF_TEXT_MODEL") or "meta-llama/Llama-3.3-70B-Instruct",
    "key_env": "HF_TOKEN",
    "prioritaet": 80,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
