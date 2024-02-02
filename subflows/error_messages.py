import random
from bot_setup import bot, Session
from utils.formatter import text_formatter


def invalid_value_type_error():
    ERROR_MESSAGES = [
        "Tem certeza que o valor inserido está correto? {bold}Por favor, tente novamente.{bold}",
        "Desculpe, não conseguimos processar essa informação. Certifique-se de fornecer valores válidos e {bold}tente novamente.{bold}",
        "Ops! Parece que recebemos um valor inesperado. Por favor, {bold}verifique os dados que você inseriu e tente novamente.{bold}"
    ]
    random_number = random.randint(0, len(ERROR_MESSAGES) - 1)
    chosen_message = ERROR_MESSAGES[random_number]

    return bot.send_message(Session.chat_id, text_formatter(chosen_message))


def custom_error_message(message: str):
    return bot.send_message(Session.chat_id, text_formatter(message))


def default_error_message():
    ERROR_MESSAGES = [
        "Ops, parece que algo não está funcionando corretamente do nosso lado. Por favor, tente novamente mais tarde.",
        "Algo estranho está acontecendo por aqui. Não consigo continuar esse fluxo, no momento.",
        "Parece que encontramos um pequeno contratempo. Não conseguimos prosseguir neste momento. Que tal tentar novamente mais tarde?",
        "Algo inesperado aconteceu e estamos com dificuldades no momento. Pedimos desculpas pelo transtorno. Pode tentar novamente mais tarde?",
        "Hmm, parece que há um probleminha por aqui. Não podemos continuar com a operação agora. Por favor, tente novamente em alguns instantes."
    ]
    random_number = random.randint(0, len(ERROR_MESSAGES)-1)
    chosen_message = ERROR_MESSAGES[random_number]

    return bot.send_message(Session.chat_id, text_formatter(chosen_message))