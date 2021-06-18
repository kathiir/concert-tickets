from datetime import datetime
from typing import Any, Dict

from sqlalchemy import and_

from auth_utils import recreate_token_for_response
from const_keys import SUCCESS_KEY, DESCRIPTION_KEY, TOKEN_NOT_FOUND
from models import Concert, db, hall_simpl_schema, Ticket, User, HallZone
from utils import check_keys_in_dict


def get_hall_with_zones(concert_id: int) -> Dict[str, Any]:
    concert = Concert.query.get(concert_id)

    response = {SUCCESS_KEY: True}

    if not concert:
        return {SUCCESS_KEY: False}

    response['concert_name'] = concert.concert_name
    response['concert_date'] = concert.concert_date.isoformat()

    response['hall'] = hall_simpl_schema.dump(concert.hall)

    result = list()

    for hall_zone in concert.hall.hall_zone:
        temp_result = {
            'price': hall_zone.price,
            'hall_zone_id': hall_zone.hall_zone_id,
            'hall_zone_name': hall_zone.hall_zone_name,
            'capacity': hall_zone.capacity
        }

        total_bought = db.session.query(Ticket) \
            .filter(and_(Ticket.concert_id == concert_id,
                         Ticket.hall_zone_id == hall_zone.hall_zone_id)) \
            .count()

        temp_result['free_capacity'] = hall_zone.capacity - total_bought

        result.append(temp_result)

    response['hall_zone'] = result

    return response


def buy_tickets_mock(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_keys = ['concert_id', 'hall_zone']

    if not check_keys_in_dict(request, approved_keys):
        raise ValueError("not approved key")

    concert = Concert.query.get(int(request['concert_id']))

    if not concert:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'concert not found'}

    if concert.concert_date <= datetime.now():
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'concert already passed'}

    if concert.concert_status:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'concert has been cancelled'}

    user = None

    if 'token' in request:
        user = db.session.query(User) \
            .filter(User.user_token == request['token']) \
            .first()

    for hall_zone in request['hall_zone']:
        zone = HallZone \
            .query \
            .get(int(hall_zone['hall_zone_id']))

        if not zone or zone not in concert.hall.hall_zone:
            db.session.flush()
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'hall zone not found'}

        total_bought = db.session.query(Ticket) \
            .filter(and_(Ticket.concert_id == concert.concert_id,
                         Ticket.hall_zone_id == int(hall_zone['hall_zone_id']))) \
            .count()

        if (zone.capacity - total_bought) < int(hall_zone['amount']):
            db.session.flush()
            return {SUCCESS_KEY: False, DESCRIPTION_KEY: 'not enough places in one concert zone'}

        for i in range(int(hall_zone['amount'])):
            ticket = Ticket(
                hall_zone=zone,
                concert=concert
            )

            if user:
                ticket.user = user

            db.session.add(ticket)

    db.session.commit()

    if 'token' in request:
        return recreate_token_for_response({SUCCESS_KEY: True},
                                           request['token'])
    return {SUCCESS_KEY: True}


# CONCERT NAME, CONCERT DATE, HALL NAME, PRICE


def get_every_possible_ticket(token: str) -> Dict[str, Any]:
    user = User.query \
        .filter(User.user_token == token) \
        .first()

    if not user:
        return {SUCCESS_KEY: False,
                DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    response = {SUCCESS_KEY: True}

    tickets = list()

    for ticket in Ticket.query \
            .filter(Ticket.user_id == user.user_id) \
            .join(Concert).join(HallZone) \
            .order_by(Concert.concert_date.desc()) \
            .order_by(HallZone.price.desc()) \
            .all():
        tickets.append(
            {'concert_id': ticket.concert.concert_id,
             'concert_name': ticket.concert.concert_name,
             'concert_date': ticket.concert.concert_date.isoformat(),
             'hall_name': ticket.concert.hall.hall_name,
             'price': ticket.hall_zone.price}
        )

    response['tickets'] = tickets

    return recreate_token_for_response(response, token)
