import traceback

from flask import render_template, request, redirect, url_for, flash

from config import app
from models import Ticket, db


@app.route('/ticket', methods=['GET'])
def ticket_find():
    placement_to_find = request.args.get("placement")

    if placement_to_find is None:
        placement_to_find = ""

    placement_search = "%{}%".format(placement_to_find)

    all_rows = Ticket.query \
        .filter(Ticket.placement.ilike(placement_search))
    return render_template("agents.html", agents=all_rows.all())  # ?


@app.route('/ticket', methods=['GET'])
def ticket():
    all_ticket = Ticket.query.all()
    return render_template("agents.html", agents=all_ticket)  # ?


@app.route('/ticket', methods=['POST'])
def add_ticket():
    try:
        placement = request.form.get('newTicketPlacement')
        new_ticket = Ticket(
            placement=placement
        )
        db.session.add(new_ticket)
        db.session.commit()
    except Exception:
        flash('Этот зал уже добавлен!')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/ticket/delete', methods=['POST'])
def delete_ticket():
    ticket_id = request.form.get('ticket_id')
    try:
        del_ticket = Ticket.query.filter(Ticket.ticket_id == ticket_id).first()
        db.session.delete(del_ticket)
        db.session.commit()
    except Exception:
        flash('Невозможно удалить')
        return redirect(url_for('agents'))  # ?
    return redirect(url_for('agents'))  # ?


@app.route('/ticket/edit', methods=['POST'])
def edit_ticket():
    try:
        curr_id = request.form.get('ticket_id')
        Ticket.query.filter(Ticket.ticket_id == curr_id).update(
            {
                'placement': request.form.get('placement'),
            })
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно внести изменение')
    return redirect(url_for('agents'))  # ?
