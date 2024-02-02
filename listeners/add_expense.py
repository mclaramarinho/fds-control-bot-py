from bot_setup import bot, Session
from firebase.read_user import has_categories_registered, get_expenses, get_budget
from models.Add_Expense_Main_Menu import AddExpenseMainMenu
from subflows.error_messages import default_error_message, custom_error_message
from firebase.update_user import update_history_add_expense
from datetime import datetime

from subflows.main_menu import main_menu, go_back_to_main_menu
from utils.formatter import text_formatter


class AddExpenseSession:
    '''
        :cvar current_step: (not_started / main_menu / pick_category / value_input / done)
        :cvar prev_step: (not_started / main_menu / pick_category / value_input / done)
    '''
    current_step = "not_started"
    prev_step = ""

    @classmethod
    def has_categories(cls):
        '''
        :returns: True - has categories to pick | False - has only the default category
        '''
        return has_categories_registered(Session.chat_id)


@bot.message_handler(func=lambda message: is_in_add_expense_session())
def handle_text_input(msg):
    if AddExpenseSession.current_step == "main_menu" or AddExpenseSession.current_step == "not_started":
        show_add_expense_menu()

    if AddExpenseSession.current_step == "value_input":
        validate_value_input(msg.text)


@bot.callback_query_handler(func=lambda call: is_in_add_expense_session())
def handle_button_input(call):
    data = call.data
    if AddExpenseSession.current_step == "value_input" or AddExpenseSession.current_step == "pick_category":
        if data == "back":
            try:
                main_menu()
                AddExpenseSession.current_step = "not_started"
                AddExpenseSession.prev_step = ""
            except Exception:
                default_error_message()


def is_in_add_expense_session():
    return Session.current_step == "add_expense"


def show_add_expense_menu():
    AddExpenseSession.prev_step = "not_started"
    AddExpenseSession.current_step = "main_menu"
    try:
        menu = AddExpenseMainMenu(AES=AddExpenseSession)
        menu_msg = menu.get_menu_message()
        menu_markup = menu.get_menu_buttons()

        bot.send_message(Session.chat_id, text=menu_msg, reply_markup=menu_markup)

        AddExpenseSession.current_step = "value_input"
        AddExpenseSession.prev_step = "main_menu"
    except Exception:
        default_error_message()
        go_back_to_main_menu(prev_step="add_expense")
        AddExpenseSession.prev_step = ""
        AddExpenseSession.current_step = "not_started"


def validate_value_input(value):
    try:
        value = value.replace(",", ".")
        parsed_value = float(value)
        was_added = update_history_add_expense(parsed_value)
        if was_added:
            added_expense_message()
        else:
            raise Exception("expense not registered")

    except Exception as e:
        custom_error_message(message="Algo aconteceu por aqui... Verifique o valor enviado e {bold}tente novamente{bold}!")
        show_add_expense_menu()


def added_expense_message():
    try:
        message_content = "Pronto! Acabei de salvar seu novo gasto.{lineBreak}{bold}Se liga nos seus gastos dessa semana:{bold}{lineBreak}"
        expense_history = get_expenses()

        planned_budget = get_budget(Session.chat_id)["budgetFinal"]

        percent_expended = expense_history["totalSpent"]

        if planned_budget != 0:
            percent_expended = (expense_history["totalSpent"] * 100) / planned_budget

        message_content += "{lineBreak}{lineBreak}Seu gasto total: R$" + str(expense_history["totalSpent"])

        message_content += "{lineBreak}{lineBreak}{bold}{italic}Gastos por categoria{italic}{bold}:"

        for cat in expense_history["categories"]:
            message_content += "{lineBreak}- " + cat + ": R$" + str(expense_history["categories"][cat])

        message_content += "{lineBreak}{lineBreak}Seu budget semanal é: R$" + str(planned_budget)
        message_content += "{lineBreak}{lineBreak}{bold}Você já gastou " + str(percent_expended) + "% do limite estabelecido.{bold}"

        message_content = text_formatter(message_content)

        bot.send_message(Session.chat_id, message_content)

        main_menu()

        AddExpenseSession.current_step = "not_started"
        AddExpenseSession.prev_step = ""
    except Exception as e:
        print(e.__str__())
        default_error_message()
        main_menu()


