import telebot

from api_cinema import api
from enums.status_command import StatusCommand

from handle import films


class HandleCommand:
    api = api.KinopoiskApi()
    status_command_now = StatusCommand.NOTHING

    films_event = films.FilmsHandle()

    def status(self, text, message, app_bot, keyboard):
        if self.status_command_now == self.status_command_now.NOTHING:
            self.handle(text=text, message=message, app_bot=app_bot, keyboard=keyboard)
        elif self.status_command_now == self.status_command_now.ENTER_NAME_FILM:
            self.status_command_now = self.status_command_now.NOTHING
            self.films_event.film_request_find(message=message, text=text, app_bot=app_bot, keyboard=keyboard)

    def handle(self, text, message, app_bot, keyboard):
        keyboard.clear_markup()
        if text == "Найти фильм по названию":
            self.status_command_now = self.status_command_now.ENTER_NAME_FILM
            app_bot.send_message(message.chat.id, "Напишите название фильма",
                                 reply_markup=keyboard.createReplyKeyboard())
        elif text == "Топ ожидаемых фильмов":
            self.films_event.create_view_list_films(message=message, app_bot=app_bot, keyboard=keyboard,
                                                    count_page=0, list_films="await_films",
                                                    func_call=self.api.get_list_await_films())
        elif text == "Топ 20 популярных фильмов":
            self.films_event.create_view_list_films(message=message, app_bot=app_bot, keyboard=keyboard,
                                                    count_page=0, list_films="top_20_films",
                                                    func_call=self.api.get_list_top_films())

    def callback_handle(self, message, text, app_bot, keyboard):
        keyboard.clear_markup()
        if text == "next_page_await_film":
            self.films_event.next_page(message=message, text="await", app_bot=app_bot, keyboard=keyboard,
                                       list_films=self.films_event.get_await_film_list(),
                                       count_page=self.films_event.get_page_await_film_count(),
                                       name_callback=["next_page_await_film", "previous_page_await_film"])
        elif text == "previous_page_await_film":
            self.films_event.previous_page(message=message, text="await", app_bot=app_bot, keyboard=keyboard,
                                           list_films=self.films_event.get_await_film_list(),
                                           count_page=self.films_event.get_page_await_film_count(),
                                           name_callback=["next_page_await_film", "previous_page_await_film"])
        elif text == "next_page_top_20_film":
            self.films_event.next_page(message=message, text="top_20", app_bot=app_bot, keyboard=keyboard,
                                       list_films=self.films_event.get_top_20_film_list(),
                                       count_page=self.films_event.get_page_top_20(),
                                       name_callback=["next_page_top_20_film", "previous_page_top_20_film"])
        elif text == "previous_page_top_20_film":
            self.films_event.previous_page(message=message, text="top_20", app_bot=app_bot, keyboard=keyboard,
                                           list_films=self.films_event.get_top_20_film_list(),
                                           count_page=self.films_event.get_page_top_20(),
                                           name_callback=["next_page_top_20_film", "previous_page_top_20_film"])
