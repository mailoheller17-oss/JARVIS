from ._basis import GRATIS, KONTINGENT, BEZAHLT, env as _env, http_test, llm_test

name = "telegram"
titel = "Telegram"
kategorie = "Messenger"
beschreibung = "Jarvis schickt dir Nachrichten per Telegram-Bot."
kosten = GRATIS
env = ['TELEGRAM_BOT_TOKEN']
key_url = "https://t.me/BotFather"


def test():
    return http_test(f"https://api.telegram.org/bot{_env('TELEGRAM_BOT_TOKEN')}/getMe")
