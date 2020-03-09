import config
from datetime import datetime
import json

try:
    open(config.db_path, "r")
except FileNotFoundError:
    with open(config.db_path, "w") as f:
        json.dump({}, f)


class Day(object):
    def __init__(self, date):
        if type(date) == str:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        else:
            self.date = date

        self.date_str = self.__repr__()
        self.load()

    def __repr__(self):
        return self.date.strftime("%Y-%m-%d")

    def load(self):
        with open(config.db_path, "r") as f:
            db = json.load(f)
            day = db.get(self.date_str, {})
            self.exercises = day.get("exercises", {})
            self.attributes = day.get("attributes", {})

    def save(self):
        day = {"exercises": self.exercises, "attributes": self.attributes}
        with open(config.db_path, "r+") as f:
            db = json.load(f)
        with open(config.db_path, "w") as f:
            db[self.date_str] = day
            json.dump(db, f)

    def to_json(self):
        day = {"date": self.date_str,
               "exercises": self.exercises,
               "attributes": self.attributes}
        return json.dumps(day)
