import telebot

from api_cinema import api


class FilmsHandle:
    api = api.KinopoiskApi()

    page_await_film_count = 0
    await_film_list = []

    page_top_20_film_count = 0
    top_20_film_list = []

    def get_page_top_20(self):
        return self.page_top_20_film_count

    def get_top_20_film_list(self):
        return self.top_20_film_list

    def get_page_await_film_count(self):
        return self.page_await_film_count

    def get_await_film_list(self):
        return self.await_film_list

    @staticmethod
    def create_markup(keyboard, count_page, list_films, name_callback):
        result_markup = keyboard.createReplyKeyboard()
        return keyboard.create_inline_keyboard(count_page, len(list_films) - 1, name_callback=name_callback)

    @staticmethod
    def json_to_string(genres_list, name_key_json):
        res = ""
        for value in genres_list:
            res += value[name_key_json] + ", "
        return res

    @staticmethod
    def class_genre_list_to_string(genres_list):
        res = ""
        for value in genres_list:
            res += value.genre + ", "
        return res

    @staticmethod
    def class_country_list_to_string(genres_list):
        res = ""
        for value in genres_list:
            res += value.country + ", "
        return res

    def change_page(self, message, app_bot, keyboard, count_page, list_films, name_callback):
        result = self.await_info_film_to_string(list_films, count_page)
        result_markup = self.create_markup(keyboard=keyboard, count_page=count_page, list_films=list_films,
                                           name_callback=name_callback)
        app_bot.edit_message_media(chat_id=message.message.chat.id,
                                   media=telebot.types.InputMedia(type='photo', media=result[1], caption=result[0]),
                                   message_id=message.message.message_id, reply_markup=result_markup)

    def next_page(self, message, text, app_bot, keyboard, list_films, count_page, name_callback):
        count_page += 1
        if count_page > len(list_films):
            count_page -= 1
        else:
            if text == "await":
                self.page_await_film_count = count_page
            else:
                self.page_top_20_film_count = count_page
            self.change_page(message=message, app_bot=app_bot, keyboard=keyboard,
                             count_page=count_page, list_films=list_films,
                             name_callback=name_callback)

    def previous_page(self, message, text, app_bot, keyboard, list_films, count_page, name_callback):
        count_page -= 1
        if count_page < 0:
            count_page += 1
        else:
            if text == "await":
                self.page_await_film_count = count_page
            else:
                self.page_top_20_film_count = count_page
            self.change_page(message=message, app_bot=app_bot, keyboard=keyboard,
                             count_page=count_page, list_films=list_films,
                             name_callback=name_callback)

    def film_info_to_string(self, current_film):
        return "🖼 Название фильма: " + (current_film.name_ru or "Отсуствует") \
               + "\nОригинальное название: " + (current_film.name_en or "Отсуствует") \
               + "\nГод выпуска: " + current_film.year \
               + "\n📊 Рейтинг: " + current_film.rating \
               + ("\n🎬 Жанр: " if len(current_film.genres) <= 1 else "🎬 Жанры: ") + (
                       self.class_genre_list_to_string(current_film.genres) or "Отсуствует") \
               + "\n🗳 Количество проголосовавших: " + str(current_film.rating_vote_count or "Отсуствует") + "\n" \
               + ("🏴 Страна: " if len(current_film.countries) <= 1 else "🏴 Страны: ") \
               + (self.class_country_list_to_string(current_film.countries) or "Отсуствует") + "\n" \
               + "\n🖍 Описание: " + current_film.description

    def await_info_film_to_string(self, await_film, page_await_film_count):
        res = ["🖼 Название фильма: " + (await_film[page_await_film_count]["nameRu"] or "Отсуствует")
               + "\nНазвание фильма в оригинале: " + (
                       await_film[page_await_film_count]["nameEn"] or "Отсуствует") + "\n"

               + ("\n🎬 Жанр: " if len(await_film[page_await_film_count]['genres']) <= 1 else "🎬 Жанры: ")
               + (self.json_to_string(await_film[page_await_film_count]['genres'], 'genre') or "Отсуствует") + "\n"

               + ("\n🏴 Страна: " if len(await_film[page_await_film_count]['countries']) <= 1 else "🏴 Страны: ")
               + (self.json_to_string(await_film[page_await_film_count]['countries'],
                                      'country') or "Отсуствует") + "\n"

               + "\n📊 Рейтинг: " + (await_film[page_await_film_count]["rating"] or "Отсуствует") + "\n"
               + "🗳 Количество проголосовавших: " + str(
            await_film[page_await_film_count]['ratingVoteCount'] or "Отсуствует") + "\n",
               await_film[page_await_film_count]["posterUrlPreview"]]
        return res

    def film_request_find(self, message, text, app_bot, keyboard):
        try:
            result_request = self.api.find_info_film(text)
            if result_request != "film_not_find":
                result_string = self.film_info_to_string(result_request)
                app_bot.send_photo(message.chat.id, result_request.poster_url, result_string,
                                   reply_markup=keyboard.createReplyKeyboard())
            else:
                app_bot.send_message(message.chat.id,
                                     "К сожалению данный фильм он не нашёл.\nПожалуйста повторите попытку позже !",
                                     reply_markup=keyboard.createReplyKeyboard())
        except RuntimeError or SystemError or Exception:
            app_bot.send_message(message.chat.id,
                                 "К сожалению данный фильм он не нашёл.\nПожалуйста повторите попытку позже !",
                                 reply_markup=keyboard.createReplyKeyboard())

    def create_view_list_films(self, message, app_bot, keyboard, count_page, list_films, func_call):
        try:
            if list_films == "await_films":
                self.await_film_list = func_call
                result_markup = self.create_markup(keyboard=keyboard, count_page=count_page, list_films=list_films,
                                                   name_callback=["next_page_await_film", "previous_page_await_film"])
                result = self.await_info_film_to_string(self.await_film_list, count_page)
            else:
                self.top_20_film_list = func_call
                result_markup = self.create_markup(keyboard=keyboard, count_page=count_page, list_films=list_films,
                                                   name_callback=["next_page_top_20_film", "previous_page_top_20_film"])
                result = self.await_info_film_to_string(self.top_20_film_list, count_page)
            app_bot.send_photo(message.chat.id, result[1], result[0], reply_markup=result_markup)

        except RuntimeError:
            app_bot.send_message(message.chat.id, "К сожалению произошла какая-то ошибка.\nПожалуйста повторите попытку позже !",
                                 reply_markup=keyboard.createReplyKeyboard())
