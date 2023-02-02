from telebot import TeleBot
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient


class ConfigBot:
    token_api_bot = 'TOKEN-API-BOT-FATHER-ENTER-HERE'

    token_api_client_kinopoisk = "TOKEN-API-UNOFFICIAL-ENTER-HERE"

    def getBot(self):
        return TeleBot(self.token_api_bot)

    def getClientApiKinopoisk(self):
        return KinopoiskApiClient(self.token_api_client_kinopoisk)
