from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "discord"
titel = "Discord-Webhook"
kategorie = "Messenger"
beschreibung = "Nachrichten in einen Discord-Kanal posten."
kosten = GRATIS
env = ['DISCORD_WEBHOOK_URL']
key_url = "https://support.discord.com/hc/de/articles/228383668"


def test():
    return http_test(_env("DISCORD_WEBHOOK_URL"))
