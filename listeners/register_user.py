from bot_setup import bot, Session
from subflows.error_messages import default_error_message
from subflows.main_menu import main_menu, go_back_to_main_menu
from utils.formatter import text_formatter
from firebase.create_user import New_User
from telebot import types

@bot.message_handler(func=lambda message: is_in_register_user_step())
def handle_register_user(msg):
    create_user(msg.text)

@bot.callback_query_handler(func=lambda call: is_in_register_user_step())
def handle_button_input(call):
    data = call.data
    if data == "voltar":
        go_back_to_main_menu("register_user")

def is_in_register_user_step():
    return Session.current_step=="register_user"


def register_user_initial():
    try:
        greeting()
        ask_name()
    except Exception:
        default_error_message()


def greeting():
    return bot.send_message(Session.chat_id,
                     text_formatter("Que legal! Para você se registrar é bem rapidinho (de verdade mesmo)."))


def ask_name():
    buttons = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("Voltar", callback_data="voltar")
    buttons.add(back_btn)
    return bot.send_message(Session.chat_id, text_formatter("Me diz seu nome:"), reply_markup=buttons)


def create_user(nickname):
    try:
        user = New_User(id=Session.chat_id, nickname=nickname)
        is_created = user.create_user()
        if is_created:
            return user_created()
        else:
            return user_not_created()
    except Exception as e:
        default_error_message()
        user_not_created()


def user_created():
    bot.send_message(Session.chat_id, text_formatter(
            "Prontinho! Criei seu usuário aqui.{lineBreak}Você precisa apenas configurar algumas coisas no próximo menu, tá?"))
    go_back_to_main_menu("register_user")


def user_not_created():
    bot.send_message(Session.chat_id, text_formatter("Não consegui criar seu usuário. Por favor, tente novamente!"))
    ask_name()