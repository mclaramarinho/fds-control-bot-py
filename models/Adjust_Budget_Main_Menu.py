from utils.formatter import text_formatter
from telebot import types
from models.Message_Templates import MessageTemplates

class Adjust_Budget_Main_Menu:
    def __init__(self, ABS):
        if ABS.has_categories():
            self._opt1 = "Limite Total"
            self._opt2 = "Limite de categoria"
            self._opt3 = "Voltar"

        if not ABS.has_categories():
            self._opt1 = "Limite Total"
            self._opt2 = "Voltar"

        self._message = MessageTemplates().pick_an_option

    def get_menu_buttons(self):
        markup = types.InlineKeyboardMarkup()
        all_btns = []

        count = 0
        for attr, val in self.__dict__.items():
            if attr != "_message":
                new_btn = types.InlineKeyboardButton(text=val, callback_data=count.__str__())
                count += 1
                all_btns.append(new_btn)

        for btn in all_btns:
            markup.add(btn)

        return markup

    def get_menu_message(self):
        return self._message
