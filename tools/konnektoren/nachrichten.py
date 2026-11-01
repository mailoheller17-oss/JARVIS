from ._basis import GRATIS, http_test

name = "nachrichten"
titel = "Nachrichten (tagesschau)"
kategorie = "Wissen"
beschreibung = "Top-Meldungen aus Deutschland und der Welt, ohne Schlüssel. Für „Was ging heute ab?“"
kosten = GRATIS
env = []
key_url = "https://www.tagesschau.de"


def test():
    return http_test("https://www.tagesschau.de/api2u/homepage/", headers={"User-Agent": "Mozilla/5.0"})
