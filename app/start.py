from config import config
from keyboard import keyboards
from handle import command


app_bot = config.ConfigBot().getBot()
keyboard = keyboards.Keyboard()
text_command_handle = command.HandleCommand()

class App:

    def start_app(self):
        app_bot.infinity_polling()

    @app_bot.message_handler(commands=['start'])
    def send_welcome(message):
        app_bot.send_message(message.chat.id, "Привет, ты запустил бота !", reply_markup=keyboard.createReplyKeyboard())

    @app_bot.message_handler(commands=['help'])
    def send_help_info(message):
        app_bot.send_message(message.chat.id, "Информация о списках команд !",
                             reply_markup=keyboard.createReplyKeyboard())

    @app_bot.message_handler(content_types=['text'])
    def send_test(message):
        text_command_handle.status(message=message, text=message.text, app_bot=app_bot, keyboard=keyboard)

    @app_bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        text_command_handle.callback_handle(message=call, text=call.data, app_bot=app_bot, keyboard=keyboard)


start = App()
start.start_app()
