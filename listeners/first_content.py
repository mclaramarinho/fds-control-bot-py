from bot_setup import bot, Session
from listeners.add_expense import show_add_expense_menu
from listeners.adjust_budget import show_adjust_budget_main_menu
from listeners.show_balance import show_balance_menu
from subflows.main_menu import main_menu, main_menu_verify_answer
from subflows.error_messages import default_error_message
from listeners.register_user import ask_name, greeting, register_user_initial


@bot.message_handler(content_types=["text"], func=lambda message: is_in_main_menu())
def handle_text_message(message):
    try:
        Session.chat_id = message.chat.id
        main_menu()
        Session.prev_step = "not_started"
    except Exception:
        default_error_message()


@bot.callback_query_handler(func=lambda call: is_in_main_menu())
def handle_button_choices(call):
    data = call.data

    if Session.current_step == "main_menu":
        Session.current_step = main_menu_verify_answer(data)
        Session.prev_step = "main_menu"

        if Session.current_step == "register_user":
            register_user_initial()

        if Session.current_step == "adjust_budget":
            show_adjust_budget_main_menu()

        if Session.current_step == "add_expense":
            show_add_expense_menu()

        if Session.current_step == "show_balance":
            show_balance_menu()


def is_in_main_menu():
    return Session.current_step == "not_started" or Session.current_step == "main_menu"
