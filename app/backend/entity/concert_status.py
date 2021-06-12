import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import ConcertStatus, db


@app.route('/concert_status', methods=['GET'])
def concert_status_find():
    concert_status_name_to_find = request.args.get("concert_status_name")

    if concert_status_name_to_find is None:
        concert_status_name_to_find = ""

    concert_status_name_search = "%{}%".format(concert_status_name_to_find)

    all_rows = ConcertStatus.query \
        .filter(ConcertStatus.concert_status_name.ilike(concert_status_name_search))
    return render_template("agents.html", agents=all_rows.all())


@app.route('/concert_status', methods=['GET'])
def concert_status():
    all_concert_status = ConcertStatus.query.all()
    return render_template("agents.html", agents=all_concert_status)


@app.route('/concert_status', methods=['POST'])
def add_concert_status():
    try:
        concert_status_name = request.form.get('newConcertStatusName')
        new_concert_status = ConcertStatus(
            concert_status_name=concert_status_name
        )
        db.session.add(new_concert_status)
        db.session.commit()
    except Exception:
        flash('Этот зал уже добавлен!')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/concert_status/delete', methods=['POST'])
def delete_concert_status():
    concert_status_id = request.form.get('concert_status_id')
    try:
        del_concert_status = ConcertStatus.query.filter(ConcertStatus.concert_status_id == concert_status_id).first()
        db.session.delete(del_concert_status)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/concert_status/edit', methods=['POST'])
def edit_concert_status():
    try:
        curr_id = request.form.get('concert_status_id')
        ConcertStatus.query.filter(ConcertStatus.concert_status_id == curr_id).update(
            {
                'concert_status_name': request.form.get('concert_status_name'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))
