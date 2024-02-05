from telebot import types
from models.Message_Templates import MessageTemplates


class Main_Menu:
    def __init__(self, is_registered=True, previous_step=""):
        if is_registered:
            self._option1 = "Ajustar Limite"
            self._option2 = "Adicionar Gasto"
            self._option3 = "Ver Saldo"

            self._message = MessageTemplates().main_menu_registered

            if previous_step == "register_user":
                self._message = MessageTemplates().main_menu_just_registered

        else:
            self._option1 = "Registrar"
            self._message = MessageTemplates().main_menu_not_registered

    def get_menu_buttons(self):
        markup = types.InlineKeyboardMarkup()
        all_menu_btns = []

        count = 0
        for attr, val in self.__dict__.items():
            if attr != "_message":
                new_btn = types.InlineKeyboardButton(text=val, callback_data=count.__str__())
                count += 1
                all_menu_btns.append(new_btn)
        for btn in all_menu_btns:
            markup.add(btn)
        return markup

    def get_menu_message(self):
        return self._message