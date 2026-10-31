from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "nvidia"
titel = "NVIDIA NIM"
kategorie = "KI-Text"
beschreibung = "NVIDIA-gehostete Modelle, Gratis-Credits zum Testen."
kosten = KONTINGENT
env = ["NVIDIA_API_KEY"]
key_url = "https://build.nvidia.com/"
llm = {
    "base_url": "https://integrate.api.nvidia.com/v1",
    "model": _env("NVIDIA_MODEL") or "meta/llama-3.3-70b-instruct",
    "key_env": "NVIDIA_API_KEY",
    "prioritaet": 70,
}


def test():
    return llm_test(llm["base_url"], llm["key_env"])
