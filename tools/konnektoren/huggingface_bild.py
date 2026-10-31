from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "huggingface_bild"
titel = "Hugging Face FLUX"
kategorie = "Bilder"
beschreibung = "Bilder mit FLUX.1-schnell über Hugging Face."
kosten = KONTINGENT
env = ['HF_TOKEN']
key_url = "https://huggingface.co/settings/tokens"


def test():
    return http_test("https://huggingface.co/api/whoami-v2", headers={"Authorization": f"Bearer {_env('HF_TOKEN')}"})
