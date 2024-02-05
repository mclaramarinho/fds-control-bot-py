from bot_setup import bot, Session
from models.Adjust_Budget_Main_Menu import Adjust_Budget_Main_Menu
from subflows.error_messages import default_error_message, invalid_value_type_error
from utils.formatter import text_formatter, money_formatter
from firebase.read_user import has_categories_registered, get_budget
from firebase.update_user import update_total_budget
from subflows.main_menu import main_menu


@bot.message_handler(func=lambda message: is_in_adjust_budget())
def handle_adjust_budget_flow(msg):
    if AdjustBudgetSession.current_step == "not_started":
        show_adjust_budget_main_menu()

    if AdjustBudgetSession.current_step == "value_input":
        validate_budget_value(msg.text)


@bot.callback_query_handler(func=lambda call: is_in_adjust_budget())
def handle_keyboard_inputs(call):
    data = call.data
    if AdjustBudgetSession.current_step == "main_menu":
        handle_main_menu_choice(data)


def is_in_adjust_budget():
    return Session.current_step == "adjust_budget"


''' --------------------------------------------------------------------------------- '''

''' STARTUP FLOW '''


def show_adjust_budget_main_menu():
    AdjustBudgetSession.current_step = "main_menu"
    menu = Adjust_Budget_Main_Menu(AdjustBudgetSession)
    menu_msg = menu.get_menu_message()
    menu_markup = menu.get_menu_buttons()
    bot.send_message(Session.chat_id, text=menu_msg, reply_markup=menu_markup)


def handle_main_menu_choice(choice):
    try:
        is_back_option = (not AdjustBudgetSession.has_categories() and choice == "1") or (
                    AdjustBudgetSession.has_categories() and choice == "2")

        if is_back_option:
            Session.current_step = "main_menu"
            Session.prev_step = "adjust_budget"
            main_menu()

        if choice == "0":  # Limite Total
            adjust_total_budget()

        if AdjustBudgetSession.has_categories():
            if choice == "1":  # Limite de categorias
                print()
                #todo: show a menu to pick categories
    except Exception as e:
        default_error_message()
        show_adjust_budget_main_menu()


''' --------------------------------------------------------------------------------- '''

''' ADJUST TOTAL BUDGET FLOW '''


def adjust_total_budget():
    try:
        previous_budget = get_budget(Session.chat_id)["budgetFinal"]
        message_content = ("Seu limite anterior: R$" + money_formatter(previous_budget)
                           + "{lineBreak}{lineBreak}{bold}Digite o novo limite de gastos:{bold}")
        bot.send_message(Session.chat_id, text_formatter(message_content))
        AdjustBudgetSession.prev_step = "main_menu"
        AdjustBudgetSession.current_step = "value_input"
    except Exception as e:
        default_error_message()
        adjust_total_budget()


def validate_budget_value(value):
    try:
        value = value.replace(",", ".")
        parsed_value = float(value)
        was_updated = update_total_budget(Session.chat_id, parsed_value)
        if was_updated:
            AdjustBudgetSession.prev_step = "value_input"
            budget_value_updated_message()
        if not was_updated:
            raise Exception("budget not updated")
    except ValueError as ve:
        invalid_value_type_error()
        adjust_total_budget()
    except TypeError as te:
        invalid_value_type_error()
        adjust_total_budget()
    except Exception as e:
        default_error_message()
        adjust_total_budget()


''' --------------------------------------------------------------------------------- '''

''' SUCCESS MESSAGE '''


def budget_value_updated_message():
    try:
        AdjustBudgetSession.current_step = "done"

        message_content = "Que legal! Seu limite foi atualizado.{lineBreak}{lineBreak}{bold}Olha aqui um resumo dos seus limites:{bold}{lineBreak}"

        budget_db = get_budget(Session.chat_id)
        categories = budget_db["categories"]

        budget_summary = "{lineBreak}{italic}LIMITE TOTAL: R${italic}" + money_formatter(budget_db["budgetFinal"])
        budget_summary += "{lineBreak}{lineBreak}{bold}{italic}LIMITE POR CATEGORIAS:{italic}{bold}"

        for category in categories:
            formatted_category = category.replace("_", " ").lower().capitalize()
            budget_summary = (budget_summary + "{lineBreak}- {bold}" + formatted_category + ":{bold} R$"
                              + money_formatter(categories[category]))

        message_content += budget_summary
        message_content = text_formatter(message_content)

        bot.send_message(Session.chat_id, message_content)

        main_menu()

        Session.prev_step = "adjust_budget"
        AdjustBudgetSession.reset_steps()
    except Exception as e:
        default_error_message()


class AdjustBudgetSession:
    '''
        :cvar current_step: (not_started / main_menu / pick_category / value_input / done)
        :cvar prev_step: (not_started / main_menu / pick_category / value_input / done)
    '''
    current_step = "not_started"
    prev_step = ""
    error_count = 0

    @classmethod
    def has_categories(cls):
        '''
        :returns: True - has categories to pick | False - has only the default category
        '''
        return has_categories_registered(Session.chat_id)

    @classmethod
    def reset_steps(cls):
        cls.prev_step = ""
        cls.current_step = "not_started"

