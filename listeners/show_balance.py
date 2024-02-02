from bot_setup import bot, Session
from models.Balance_Menu import BalanceMenu
from subflows.error_messages import default_error_message
from subflows.main_menu import go_back_to_main_menu


@bot.callback_query_handler(func=lambda call: is_in_show_balance_step())
def handle_button_input(call):
    data = call.data
    if data == "voltar":
        go_back_to_main_menu("show_balance")


@bot.message_handler(func=lambda msg: is_in_show_balance_step())
def handle_text_input(msg):
    if msg.text == "voltar" or msg.text == "Voltar" or "1":
        go_back_to_main_menu("show_balance")
    else:
        try:
            default_error_message()
        except Exception as e:
            bot.send_message(Session.chat_id, "Desculpe, algo muito errado está acontecendo aqui no servidor... Por favor, fale comigo mais tarde.")
            bot.stop_polling()
            bot.polling()


def is_in_show_balance_step():
    return Session.current_step == "show_balance"


def show_balance_menu():
    menu = BalanceMenu()
    menu_msg = menu.get_balance_summary()
    menu_btn = menu.get_buttons()
    bot.send_message(Session.chat_id, text=menu_msg, reply_markup=menu_btn)
