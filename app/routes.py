from app import app
from flask import render_template
from journal import Day
from datetime import datetime, timedelta
from flask import request


@app.route('/', methods=['GET', 'POST'])
def journal():
    if request.method == "POST":
        return "{}".format(str(request.form))
    elif {"day", "month", "year"}.issubset(request.args.keys()):
        year = int(request.args.get("year"))
        month = int(request.args.get("month"))
        day = int(request.args.get("day"))
        if request.args.get("plus"):
            date = datetime(year, month, day)
            date += timedelta(days=1)
            year, month, day = date.year, date.month, date.day
        if request.args.get("minus"):
            date = datetime(year, month, day)
            date -= timedelta(days=1)
            year, month, day = date.year, date.month, date.day
        day = Day(year, month, day)
        return render_template('form.html', day=day)
    else:
        now = datetime.now()
        day = Day(now.year, now.month, now.day)
        return render_template('form.html', day=day)
