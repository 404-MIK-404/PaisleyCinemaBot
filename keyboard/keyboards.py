from telebot import types


class Keyboard:

    markup = ""

    def createReplyKeyboard(self):
        self.markup = types.ReplyKeyboardMarkup()
        context_keyboard = [["Найти фильм по названию", "find_film"],
                            ["Топ ожидаемых фильмов", "top_await_films"],
                            ["Топ 20 популярных фильмов", "get_list_cinema_popular_cinema_20"]]
        for values in context_keyboard:
            self.markup.add(types.InlineKeyboardButton(values[0], callback_data=values[1]))
        self.markup.resize_keyboard = True
        return self.markup

    def clear_markup(self):
        self.markup = types.ReplyKeyboardRemove()

    def create_inline_keyboard(self, page_count, len_page,name_callback):
        self.markup = types.InlineKeyboardMarkup()
        context_keyboard = [["Вперёд", name_callback[0]], ["Назад", name_callback[1]]]
        if page_count == 0:
            self.markup.row(types.InlineKeyboardButton(context_keyboard[0][0], callback_data=context_keyboard[0][1]))
        if page_count == len_page:
            self.markup.row(types.InlineKeyboardButton(context_keyboard[1][0], callback_data=context_keyboard[1][1]))
        if 0 < page_count < len_page:
            self.markup.row(types.InlineKeyboardButton(context_keyboard[1][0], callback_data=context_keyboard[1][1]),
                            types.InlineKeyboardButton(context_keyboard[0][0], callback_data=context_keyboard[0][1]))
        return self.markup
