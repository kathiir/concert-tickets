import traceback

from flask import render_template, request, redirect, url_for, flash

from back import db, app
from models import City


@app.route('/city', methods=['GET'])
def city_find():
    city_name_to_find = request.args.get("city_name")

    if city_name_to_find is None:
        city_name_to_find = ""

    city_name_search = "%{}%".format(city_name_to_find)

    all_rows = City.query \
        .filter(City.city_name.ilike(city_name_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/city', methods=['GET'])
def city():
    all_city = City.query.all()
    return render_template("agents.html", agents=all_city)  # ?


@app.route('/city', methods=['POST'])
def add_city():
    try:
        city_name = request.form.get('newCityName')
        new_city = City(
            city_name=city_name
        )
        db.session.add(new_city)
        db.session.commit()
    except Exception:
        flash('Этот зал уже добавлен!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/city/delete', methods=['POST'])
def delete_city():
    city_id = request.form.get('city_id')
    try:
        del_city = City.query.filter(City.city_id == city_id).first()
        db.session.delete(del_city)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/city/edit', methods=['POST'])
def edit_city():
    try:
        curr_id = request.form.get('city_id')
        City.query.filter(City.city_id == curr_id).update(
            {
                'city_name': request.form.get('city_name'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
