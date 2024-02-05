from bot_setup import Session
from firebase.setup import Firebase_Config
from firebase.read_user import has_categories_registered, get_categories
from utils.date_utilities import get_week_number, get_month_and_year
db = Firebase_Config().db()


def update_total_budget(id:int, value:float):
    try:
        prev_limit = db.child(id).child("budget").child("budgetFinal").get().val()

        db.child(id).child("budget").child("budgetFinal").set(value)

        if has_categories_registered(id):
            categories = get_categories(id)
            sum = 0
            for category in categories:
                percent = (categories[category] * 100) / prev_limit
                current_category_value = (value * percent) / 100
                db.child(id).child("budget").child("categories").child(category).set(current_category_value)
                sum += current_category_value
        else:
            db.child(id).child("budget").child("categories").set({"Saldo_Livre": value})
        return True
    except Exception as e:
        print(e.__str__())
        return False


def update_history_add_expense(value: float, category=""):

    try:
        id = Session.chat_id

        month_year = get_month_and_year()
        week_no = get_week_number()
        total_spent = value


        history_data = db.child(id).child("history").get().val()
        print(history_data)
        global data
        data = {
                "history": {
                    month_year: {
                        week_no: {
                            "categories": {},
                            "totalSpent": total_spent
                        }
                    }
                }
            }

        global db_ref
        global data_to_send
        db_ref = None
        data_to_send = {}
        if history_data != None:
            month_year_data =  db.child(id).child("history").child(month_year).get().val()

            if month_year_data != None:
                week_no_data = db.child(id).child("history").child(month_year).child(week_no).get().val()

                if week_no_data != None:
                    total_spent = value + db.child(id).get().val()["history"][month_year][week_no]["totalSpent"]
                    data["history"][month_year][week_no]["totalSpent"] = total_spent
                    data_to_send = set_categories(data, month_year, week_no, category, total_spent, value, get_from_db=True)["history"][month_year][week_no]
                    db_ref = db.child(id).child("history").child(month_year).child(week_no)
                else:
                    data_to_send = set_categories(data, month_year, week_no, category, total_spent, value)["history"][month_year][week_no]
                    db_ref = db.child(id).child("history").child(month_year).child(week_no)
            else:
                data_to_send = set_categories(data, month_year, week_no, category, total_spent, value)["history"][month_year]
                db_ref = db.child(id).child("history").child(month_year)
        else:
            db_ref = db.child(id).child("history")
            data_to_send = set_categories(data, month_year, week_no, category, total_spent, value)["history"]

        db_ref.update(data_to_send)
        return True

    except Exception as e:
        return False


def set_categories(data, month_year, week_no, category, total_spent, value, get_from_db = False):

    if not get_from_db:
        categories = get_categories()
        for cat in categories:
            data["history"][month_year][week_no]["categories"][cat] = 0
    else:
        categories = db.child(Session.chat_id).get().val()
        categories = categories["history"][month_year][week_no]["categories"]
        for cat in categories:
            data["history"][month_year][week_no]["categories"][cat] = categories[cat]

    if len(category) == 0:
        data["history"][month_year][week_no]["categories"]["Saldo_Livre"] = total_spent
    else:
        data["history"][month_year][week_no]["categories"][category] += value

    return data
