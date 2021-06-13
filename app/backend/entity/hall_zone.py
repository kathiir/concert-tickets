import traceback

from config import app
from flask import render_template, request, redirect, url_for, flash
from models import HallZone, db


@app.route('/hall_zone', methods=['GET'])
def hall_zone_find():
    hall_zone_name_to_find = request.args.get("hall_zone_name")

    if hall_zone_name_to_find is None:
        hall_zone_name_to_find = ""

    hall_zone_name_search = "%{}%".format(hall_zone_name_to_find)

    all_rows = HallZone.query \
        .filter(HallZone.hall_zone_name.ilike(hall_zone_name_search))
    return render_template("agents.html", agents=all_rows.all())


@app.route('/hall_zone', methods=['GET'])
def hall_zone():
    all_hall_zone = HallZone.query.all()
    return render_template("agents.html", agents=all_hall_zone)


@app.route('/hall_zone', methods=['POST'])
def add_hall_zone():
    try:
        hall_zone_name = request.form.get('newHallZoneName')
        new_hall_zone = HallZone(
            hall_zone_name=hall_zone_name
        )
        db.session.add(new_hall_zone)
        db.session.commit()
    except Exception:
        flash('Этот зал уже добавлен!')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/hall_zone/delete', methods=['POST'])
def delete_hall_zone():
    hall_zone_id = request.form.get('hall_zone_id')
    try:
        del_hall_zone = HallZone.query.filter(HallZone.hall_zone_id == hall_zone_id).first()
        db.session.delete(del_hall_zone)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/hall_zone/edit', methods=['POST'])
def edit_hall_zone():
    try:
        curr_id = request.form.get('hall_zone_id')
        HallZone.query.filter(HallZone.hall_zone_id == curr_id).update(
            {
                'hall_zone_name': request.form.get('hall_zone_name'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))
