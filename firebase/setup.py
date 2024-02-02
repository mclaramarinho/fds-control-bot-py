import pyrebase
from os import environ

firebaseConfig = {
  "apiKey": environ["FB_API_KEY"],
  "authDomain": environ["FB_APP_ID"] + ".firebaseapp.com",
  "databaseURL": "https://fdscontrolofficial-default-rtdb.firebaseio.com",
  "projectId": environ["FB_APP_ID"],
  "storageBucket": environ["FB_APP_ID"] + ".appspot.com",
  "messagingSenderId": environ["FB_MESSAGING_SENDER_ID"],
  "appId": environ["FB_APP_ID"]
}


class Firebase_Config:
  def __init__(self):
    self._fba = pyrebase.initialize_app(firebaseConfig)
    self._db = self._fba.database()

  def db(self):
    return self._db
