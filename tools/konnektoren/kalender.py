from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "kalender"
titel = "Kalender (ICS)"
kategorie = "Alltag"
beschreibung = "Termine aus einer geheimen ICS-Adresse (Google/Apple), vorbereitet."
kosten = GRATIS
env = ['KALENDER_ICS_URL']
key_url = "https://support.google.com/calendar/answer/37648"


def test():
    return http_test(_env("KALENDER_ICS_URL"), ok="Kalender lesbar")
