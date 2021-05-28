import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import Hall, db


@app.route('/hall', methods=['GET'])
def hall_find():
    hall_name_to_find = request.args.get("hall_name")
    hall_address_to_find = request.args.get("hall_address")

    if hall_name_to_find is None:
        hall_name_to_find = ""
    if hall_address_to_find is None:
        hall_address_to_find = ""

    hall_name_search = "%{}%".format(hall_name_to_find)
    hall_address_search = "%{}%".format(hall_address_to_find)

    all_rows = Hall.query \
        .filter(Hall.hall_name.ilike(hall_name_search)) \
        .filter(Hall.hall_info.ilike(hall_address_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/hall', methods=['GET'])
def hall():
    all_hall = Hall.query.all()
    return render_template("agents.html", agents=all_hall)  # ?


@app.route('/hall', methods=['POST'])
def add_hall():
    try:
        hall_name = request.form.get('newHallName')
        hall_address = request.form.get('newHallAddress')
        new_hall = Hall(
            hall_name=hall_name,
            hall_address=hall_address
        )
        db.session.add(new_hall)
        db.session.commit()
    except Exception:
        flash('Этот зал уже добавлен!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/hall/delete', methods=['POST'])
def delete_hall():
    hall_id = request.form.get('hall_id')
    try:
        del_hall = Hall.query.filter(Hall.hall_id == hall_id).first()
        db.session.delete(del_hall)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/hall/edit', methods=['POST'])
def edit_hall():
    try:
        curr_id = request.form.get('hall_id')
        Hall.query.filter(Hall.hall_id == curr_id).update(
            {
                'hall_name': request.form.get('hall_name'),
                'hall_address': request.form.get('hall_address'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
