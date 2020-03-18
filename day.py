import config
from datetime import datetime
import json


class Day(object):
    def __init__(self, date, clean=False):
        if type(date) == str:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        else:
            self.date = date

        self.date_str = self.__repr__()
        if clean:
            self.attributes = {}
            self.exercises = {}
            self.exercise_order = {}
        else:
            self.load()
        self.potential_catch_up = ["1", "2"]

    def __repr__(self):
        return self.date.strftime("%Y-%m-%d")

    def load(self):
        try:
            with open(config.db_path, "r") as f:
                db = json.load(f)
                day = db.get(self.date_str, {})
                self.attributes = day.get("attributes", {})
                self.exercises = day.get("exercises", {})
                self.exercise_order = day.get("exercise_order",
                                              list(self.exercises.keys()))
        except FileNotFoundError:
            with open(config.db_path, "w") as f:
                json.dump({}, f)
            self.load()

    def save(self):
        day = {"exercises": self.exercises, "attributes": self.attributes,
               "exercise_order": self.exercise_order}
        with open(config.db_path, "r+") as f:
            db = json.load(f)
        with open(config.db_path, "w") as f:
            db[self.date_str] = day
            json.dump(db, f)
