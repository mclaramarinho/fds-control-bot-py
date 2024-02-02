from firebase.setup import Firebase_Config

class New_User:
    def __init__(self, id, nickname):
        self._chat_id = id
        self._nickname = nickname
        self._total_budget = 0
        self._initial_category = "Saldo Livre"
        self._initial_category_value = 0
        self._new_user_data = {
            "budget":{
                "budgetFinal": 0,
                "categories":{
                    self._initial_category.replace(" ", "_"): self._initial_category_value
                },
            },
            "chatID": self._chat_id,
            "nickname": self._nickname
        }

    def create_user(self):
        db = Firebase_Config().db()
        try:
            db.child(self._chat_id).set(self._new_user_data)
            return True
        except Exception as e:
            print(e.__str__())
            return False
