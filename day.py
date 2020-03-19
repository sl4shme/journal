import config
from datetime import datetime, timedelta
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
            self.exercises_order = []
            self.total = 0
            self.potential_catch_up = []
            self.caught_up = ""
        else:
            self.load()

    def __repr__(self):
        return self.date.strftime("%Y-%m-%d")

    def compute_total(self):
        if self.caught_up != "":
            return 1
        total = 0
        for exercise in self.exercises.values():
            if exercise.get("catch_up", "") == "":
                total += float(exercise.get("counts", 0))
        return total

    def check_catch_up(self, db, date):
        if date != "":
            day = db.get(date, {})
            for exercise in day.get("exercises").values():
                if exercise.get("catch_up", "") == self.date_str:
                    self.caught_up = date
                    return
            self.caught_up = ""
            self.save()
        self.caught_up = ""

    def apply_catch_up(self):
        for exercise in self.exercises.values():
            if exercise["catch_up"] != "":
                older_day = Day(exercise["catch_up"])
                older_day.caught_up = self.date_str
                older_day.save()

    def compute_catch_up(self, db, start=None):
        potential_catch_up = []
        for exercise in self.exercises.values():
            if exercise.get("catch_up", "") != "":
                potential_catch_up.append(exercise["catch_up"])
        if start is None:
            start = datetime(day=1, month=1, year=self.date.year)
        while start < self.date:
            name = start.strftime("%Y-%m-%d")
            day = db.get(name, {})
            if day.get("total", 0) < 1:
                potential_catch_up.append(name)
            start += timedelta(days=1)
        return potential_catch_up

    def load(self):
        try:
            with open(config.db_path, "r") as f:
                db = json.load(f)
                day = db.get(self.date_str, {})
                self.attributes = day.get("attributes", {})
                self.exercises = day.get("exercises", {})
                self.exercises_order = day.get("exercises_order",
                                               list(self.exercises.keys()))
                self.total = day.get("total", 0)
                self.check_catch_up(db, day.get("caught_up", ""))
                self.potential_catch_up = self.compute_catch_up(db)

        except FileNotFoundError:
            with open(config.db_path, "w") as f:
                json.dump({}, f)
            self.load()

    def save(self):
        self.apply_catch_up()
        day = {"exercises": self.exercises,
               "attributes": self.attributes,
               "exercises_order": self.exercises_order,
               "total": self.compute_total(),
               "caught_up": self.caught_up}
        with open(config.db_path, "r+") as f:
            db = json.load(f)
        with open(config.db_path, "w") as f:
            db[self.date_str] = day
            json.dump(db, f)
