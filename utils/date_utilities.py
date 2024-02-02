from datetime import datetime


def get_month_and_year():
    today = datetime.today()

    month = str(today.month)
    year = str(today.year)
    return f"{month}-{year}"


def get_week_number():
    today = datetime.today()
    week_no = str(today.isocalendar()[1])

    return f"week{week_no}"