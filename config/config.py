from telebot import TeleBot
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient


class ConfigBot:
    token_api_bot = '5743901649:AAHNYlpXm4sUx0vWVGdZadtvEP6cmTCFVEw'

    token_api_client_kinopoisk = "04cf1757-8fc4-4ed9-9ac0-08af7a7275f8"

    def getBot(self):
        return TeleBot(self.token_api_bot)

    def getClientApiKinopoisk(self):
        return KinopoiskApiClient(self.token_api_client_kinopoisk)
