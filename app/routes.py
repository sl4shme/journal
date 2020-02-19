from app import app
from flask import render_template
from journal import Day
from datetime import datetime, timedelta
from flask import request


@app.route('/', methods=['GET', 'POST'])
def journal():
    if request.method == "POST":
        f = request.form.to_dict()
        day = Day(f['date'])
        day.recap = f['recap']
        day.exercises = {}
        for ex_id in set([k.split("_")[1] for k in f.keys()
                          if k.startswith("ex_")]):
            ex = {}
            for key, val in [("_".join(k.split("_")[2:]), f[k])
                             for k in f.keys()
                             if k.startswith("ex_{}".format(ex_id))]:
                ex[key] = val
            day.exercises[ex_id] = ex

        return "{} {}".format(str(day), str(day.exercises))

    elif "date" in request.args.keys():
        try:
            date = datetime.strptime(request.args['date'], '%Y-%m-%d')
        except ValueError:
            date = datetime.now()
        if request.args.get("plus"):
            date += timedelta(days=1)
        if request.args.get("minus"):
            date -= timedelta(days=1)
        day = Day(date)
        return render_template('form.html', day=day)

    else:
        day = Day(datetime.now())
        return render_template('form.html', day=day)
