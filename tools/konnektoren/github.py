from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "github"
titel = "GitHub"
kategorie = "Entwickler"
beschreibung = "Repos, Issues und Codespaces."
kosten = GRATIS
env = ['GITHUB_TOKEN']
key_url = "https://github.com/settings/tokens"


def test():
    return http_test("https://api.github.com/rate_limit", headers={"Authorization": f"Bearer {_env('GITHUB_TOKEN')}"})
