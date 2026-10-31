from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "mixkit"
titel = "Mixkit"
kategorie = "Material"
beschreibung = "Gratis Musik, SFX und Videoclips (ohne API, Jarvis verlinkt passende Seiten)."
kosten = GRATIS
env = []
key_url = "https://mixkit.co/"


def test():
    return http_test("https://mixkit.co/free-sound-effects/", ok="erreichbar")
