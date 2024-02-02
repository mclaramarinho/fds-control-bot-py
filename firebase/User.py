from firebase.setup import Firebase_Config
from utils.date_utilities import get_week_number, get_month_and_year

db = Firebase_Config().db()


class User:
    @property
    def uid(self):
        return self._uid

    @property
    def nickname(self):
        return self._nickname

    @property
    def budget_limit(self):
        return self._budget_limit

    @property
    def categories_registered(self):
        return self._categories_registered

    @property
    def history (self):
        return self._history

    @property
    def user_has_history(self):
        return self._user_has_history

    @property
    def current_week_expense(self):
        return self._current_week_expense

    def __init__(self, chat_id : int):
        try:
            is_user_registered = find_user(chat_id)
            if is_user_registered:
                user_info = get_user_info(chat_id)
                self._nickname = user_info["nickname"]
                self._uid = user_info["chatID"]
                self._budget_limit = user_info["budget"]["budgetFinal"]
                categories = user_info["budget"]["categories"]
                self._categories_registered = []

                for cat in categories:
                    formatted_category = cat.replace("_", " ")
                    formatted_category = formatted_category.lower()
                    formatted_category = formatted_category[0].upper() + formatted_category[1:]

                    self._categories_registered.append(formatted_category)

                user_has_history = has_history(chat_id)

                self._user_has_history = user_has_history

                if user_has_history:
                    self._history = get_history(chat_id)
                    self._current_week_expense = get_expenses(chat_id)

        except Exception as e:
            print(e.__str__())

    def update_user(self):
        try:
            self.__init__(chat_id=self._uid)
            return True
        except Exception as e:
            return False





def find_user(id):
    try:
        user_info = db.child(id).get()
        if user_info.val() == None:
            raise Exception("User does not exist.")
        return True #exists
    except Exception as e:
        if e.__str__() == "User does not exist.":
            return False #not exists


def get_user_info(id):

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


def get_categories(id):
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

def get_expenses(id):
    id = Session.chat_id
    month_year = get_month_and_year()
    week_no = get_week_number()

    try:
        history = db.child(id).get().val()["history"][month_year][week_no]
        return history
    except Exception as e:
        print(e.__str__())
        return {}


def has_history(id):
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


def get_history(id):
    id = Session.chat_id
    try:
        history = db.child(id).get().val()["history"]
        if history == None:
            return False
        else:
            return history
    except Exception as e:
        return False

