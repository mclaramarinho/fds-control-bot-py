from firebase.read_user import get_categories
from utils.formatter import text_formatter
from telebot import types
from bot_setup import Session
from models.Message_Templates import MessageTemplates

class AddExpenseMainMenu:
    def __init__(self, AES):
        self._message = MessageTemplates().insert_value

        if AES.has_categories():
            categories = get_categories()
            self._categories = []
            self._message = MessageTemplates().pick_an_option

            for category in categories:
                self._categories.append(category)

            self._back = "Voltar"

        if not AES.has_categories():
            self._back = "Voltar"


    def get_menu_buttons(self):
        markup = types.InlineKeyboardMarkup()
        all_btns = []

        count = 0
        for attr, val in self.__dict__.items():
            if attr != "_message" and attr != "_back":
                new_btn = types.InlineKeyboardButton(text=val, callback_data=count.__str__())
                count += 1
                all_btns.append(new_btn)

        back_btn = types.InlineKeyboardButton(text=self._back, callback_data="back")
        all_btns.append(back_btn)

        for btn in all_btns:
            markup.add(btn)

        return markup

    def get_menu_message(self):
        return self._message
