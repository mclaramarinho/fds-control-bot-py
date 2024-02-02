from bot_setup import bot, Session
from listeners import first_content, register_user, adjust_budget, show_balance, add_expense


if __name__ == '__main__':
    bot.polling()
