from firebase.setup import Firebase_Config
from bot_setup import Session
from utils.date_utilities import get_week_number, get_month_and_year

db = Firebase_Config().db()

def find_user(id):
    try:
        user_info = db.child(id).get()
        if user_info.val() == None:
            raise Exception("User does not exist.")
        return True #exists
    except Exception as e:
        if e.__str__() == "User does not exist.":
            return False #not exists


def get_user_info():
    id = Session.chat_id
    try:
        user_info = db.child(id).get()
        if user_info.val() == None:
            raise Exception("User does not exist.")
        return user_info.val()
    except Exception as e:
        return False


def has_categories_registered(id):
    try:
        categories_registered = db.child(id).get().val()["categories"]

        if len(categories_registered) > 1:
            return True
        else:
            return False
    except Exception as e:
        print(e.__str__())
        return False


def get_categories():
    id = Session.chat_id
    try:
        categories = db.child(id).get().val()["budget"]["categories"]
        return categories
    except Exception as e:
        return {}


def get_budget(id):
    try:
        budget = db.child(id).get().val()
        return budget["budget"]
    except Exception as e:
        return {}

def get_expenses():
    id = Session.chat_id
    month_year = get_month_and_year()
    week_no = get_week_number()
    try:
        history = db.child(id).get().val()["history"][month_year][week_no]
        return history
    except Exception as e:
        print(e.__str__())
        return None


def has_history():
    id = Session.chat_id
    try:
        history = db.child(id).get().val()["history"]
        if history == None:
            return False
        else:
            return True
    except Exception as e:
        print(e.__str__())
        return False


def get_history():
    id = Session.chat_id
    try:
        history = db.child(id).get().val()["history"]
        if history == None:
            return False
        else:
            return history
    except Exception as e:
        return False