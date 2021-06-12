import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import Concert, db


@app.route('/concert', methods=['GET'])
def concert_find():
    concert_name_to_find = request.args.get("concert_name")
    concert_info_to_find = request.args.get("concert_info")
    concert_photo_to_find = request.args.get("concert_photo")
    concert_date_to_find = request.args.get("concert_date")

    if concert_name_to_find is None:
        concert_name_to_find = ""
    if concert_info_to_find is None:
        concert_info_to_find = ""
    if concert_photo_to_find is None:
        concert_photo_to_find = ""
    if concert_date_to_find is None:
        concert_photo_to_find = ""

    concert_name_search = "%{}%".format(concert_name_to_find)
    concert_info_search = "%{}%".format(concert_info_to_find)
    concert_photo_search = "%{}%".format(concert_photo_to_find)
    concert_date_search = "%{}%".format(concert_date_to_find)

    all_rows = Concert.query \
        .filter(Concert.concert_name.ilike(concert_name_search)) \
        .filter(Concert.concert_info.ilike(concert_info_search)) \
        .filter(Concert.concert_photo.ilike(concert_photo_search)) \
        .filter(Concert.concert_date.ilike(concert_date_search))
    return render_template("agents.html", agents=all_rows.all())


@app.route('/concert', methods=['GET'])
def concert():
    all_concert = Concert.query.all()
    return render_template("agents.html", agents=all_concert)


@app.route('/concert', methods=['POST'])
def add_concert():
    try:
        concert_name = request.form.get('newConcertName')
        concert_info = request.form.get('newConcertInfo')
        concert_photo = request.form.get('newConcertPhoto')
        concert_date = request.form.get('newConcertDate')
        new_concert = Concert(
            concert_name=concert_name,
            concert_info=concert_info,
            concert_photo=concert_photo,
            concert_date=concert_date
        )
        db.session.add(new_concert)
        db.session.commit()
    except Exception:
        flash('Этот концерт уже добавлен!')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/concert/delete', methods=['POST'])
def delete_concert():
    concert_id = request.form.get('concert_id')
    try:
        del_concert = Concert.query.filter(Concert.concert_id == concert_id).first()
        db.session.delete(del_concert)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))
    return redirect(url_for('agents'))


@app.route('/concert/edit', methods=['POST'])
def edit_concert():
    try:
        curr_id = request.form.get('concert_id')
        Concert.query.filter(Concert.concert_id == curr_id).update(
            {
                'concert_name': request.form.get('concert_name'),
                'concert_info': request.form.get('concert_info'),
                'concert_photo': request.form.get('concert_photo'),
                'concert_date': request.form.get('concert_date'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))
