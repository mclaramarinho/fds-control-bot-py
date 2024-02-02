import telebot
import os
from dotenv import load_dotenv
from firebase.User import User

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MarkdownV2")


class Session:
    @property
    def user (self):
        return self._user

    chat_id = 0
    prev_step = ""
    current_step = "not_started"
    _user = None

    @classmethod
    def create_user_session(cls):
        cls._user = User(cls.chat_id)

