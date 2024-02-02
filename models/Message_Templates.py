from utils.formatter import text_formatter


class MessageTemplates:
    @property
    def main_menu_not_registered(self):
        return text_formatter("Oiê! Seja bem-vindo ao FDSControl.{lineBreak}{lineBreak}Aqui você pode controlar suas "
                             "finanças de maneira fácil!{lineBreak}{lineBreak}{bold}Você ainda não está registrado.{"
                             "bold}{lineBreak}{lineBreak}{bold}Gostaria de se registrar?{bold}")
    @property
    def main_menu_registered(self):
        return text_formatter("Oi, de novo :D{lineBreak}{bold}Como posso te ajudar agora?{bold}")

    @property
    def main_menu_just_registered(self):
        return text_formatter("{bold}Como posso te ajudar agora?{bold}")

    @property
    def pick_an_option(self):
        return text_formatter("Escolha uma das opções: ")

    @property
    def insert_value(self):
        return text_formatter("Digite o valor gasto ou clique em voltar: ")