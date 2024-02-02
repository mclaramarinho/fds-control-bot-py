from bot_setup import bot, Session
from firebase.read_user import find_user
from models.Main_Menu import Main_Menu
from subflows.error_messages import default_error_message


def main_menu():
    try:
        is_chat_id_registered = find_user(Session.chat_id)

        if is_chat_id_registered and Session.prev_step == "register_user":
            Session.create_user_session()

        menu = Main_Menu(is_chat_id_registered, previous_step=Session.prev_step)
        menu_msg = menu.get_menu_message()
        menu_options = menu.get_menu_buttons()

        bot.send_message(Session.chat_id, text=menu_msg, reply_markup=menu_options)
        Session.current_step = "main_menu"
    except Exception as e:
        default_error_message()
        go_back_to_main_menu(Session.current_step)


def main_menu_verify_answer(button_id : str):
    is_chat_id_registered = find_user(Session.chat_id)

    # if this current chat id doesn't exist
    if not is_chat_id_registered:
        if button_id == "0":
            return "register_user"
        else:
            return "invalid"

    if is_chat_id_registered:
        if button_id == "0":
            return "adjust_budget"
        elif button_id == "1":
            return "add_expense"
        elif button_id == "2":
            return "show_balance"
        else:
            return "invalid"


def go_back_to_main_menu(prev_step : str):
    try:
        Session.prev_step = prev_step
        main_menu()
    except Exception as e:
        default_error_message()
