import json
import os
import sys

repo_dir = "./repo/"


class Day(object):
    def __init__(self, year, month, day):
        self.path = "{}/{}_{}_{}.json".format(repo_dir, year, month, day)
        self.year = year
        self.month = month
        self.day = day
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.json = json.loads(f.read())
        else:
            self.json = {}

    def __repr__(self):
        return "{} / {} / {}".format(self.year, self.month, self.day)

    def write(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.json))


if __name__ == "__main__":
    d = Day(sys.argv[1], sys.argv[2], sys.argv[3])
    print(d.json)
    d.json["journal"] = sys.argv[4]
    print(d.json)
    d.write()
