from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

import shutil

name = "claude_code"
titel = "Claude Code CLI"
kategorie = "KI-Text"
beschreibung = "Nutzt die lokal angemeldete Claude-Code-CLI (dein Abo/Kontingent)."
kosten = BEZAHLT
env = []
key_url = "https://docs.claude.com/en/docs/claude-code/setup"
hinweis = "Verbraucht dein Claude-Abo bzw. API-Guthaben."
llm = {"cli": "claude", "prioritaet": 90}


def bereit():
    return bool(shutil.which("claude"))


def test():
    return (True, "CLI gefunden") if bereit() else (False, "claude nicht installiert")
