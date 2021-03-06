from app import app
from flask import render_template
from day import Day
from datetime import datetime, timedelta
from flask import request


@app.route('/', methods=['GET', 'POST'])
def journal():
    if request.method == "POST":
        f = request.form.to_dict()
        day = Day(f.pop('date'), clean=True)
        f.pop('submit')

        for ex_id in set(["_".join(k.split("_")[0:2]) for k in f.keys()
                          if k.startswith("ex_")]):
            ex = {}
            for key, val in [("_".join(k.split("_")[2:]), f[k])
                             for k in f.keys()
                             if k.startswith(ex_id)]:
                ex[key] = val
                f.pop("{}_{}".format(ex_id, key))
            day.exercises[ex_id] = ex

        for key in list(f.keys()):
            day.attributes[key] = f.pop(key)

        day.exercises_order = sorted(list(day.exercises.keys()),
                                     key=lambda k: int(day.exercises[k]["order"]))

        msg = " {} / {} / {} / {}".format(str(day),
                                          str(day.attributes),
                                          str(day.exercises),
                                          str(day.exercises_order))

        day.save()

        day = Day(day.date)

        return render_template('form.html', day=day, msg=msg)

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
