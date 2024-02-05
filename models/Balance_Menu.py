from bot_setup import Session
from firebase.read_user import get_budget, has_history, get_expenses
from utils.formatter import text_formatter, money_formatter
from telebot import types


class BalanceMenu:
    def __init__(self):
        self._budget_limit = get_budget(Session.chat_id)["budgetFinal"]
        self._total_spent = 0
        self._percent_spent = 0
        self._total_spent_msg = "{bold}Você gastou: {bold}R$"
        self._btn_1 = "Voltar"
        self._balance = 0
        user_has_history = has_history()

        if user_has_history:
            expenses = get_expenses()
            if expenses != None:
                self._total_spent += get_expenses()["totalSpent"]
            else:
                self._total_spent = 0

        if self._budget_limit != 0 and self._total_spent != 0:
            self._percent_spent = (self._total_spent * 100)/self._budget_limit

        if self._budget_limit > 0 and self._budget_limit > self._total_spent:
            self._total_spent_msg = "{bold}Você já gastou:{bold} R$"

        self._balance = abs(self._budget_limit - self._total_spent)

    def get_balance_summary(self):
        message = "**** {bold}SALDO SEMANAL{bold} ****"
        message += "{lineBreak}{lineBreak}Seu {bold}limite de gastos: R${bold}" + money_formatter(self._budget_limit)

        self._total_spent_msg += money_formatter(self._total_spent)

        message += "{lineBreak}{lineBreak}" + self._total_spent_msg

        currency_sign = "R$ " if (self._budget_limit >= self._total_spent) else "–R$ "

        message += ("{lineBreak}{lineBreak} Seu saldo é: "
                    + currency_sign
                    + money_formatter(self._balance))

        message = text_formatter(message)

        return message

    def get_buttons(self):
        back_button = types.InlineKeyboardButton(self._btn_1, callback_data="voltar")
        markup = types.InlineKeyboardMarkup().add(back_button)
        return markup

