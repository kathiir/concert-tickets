import json
from datetime import timedelta

from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from typing import Any, Dict

from auth_utils import recreate_token_for_response
from const_keys import TOKEN_NOT_FOUND, SUCCESS_KEY, DESCRIPTION_KEY
from models import User, db, Concert
from utils import check_keys_in_dict

scopes = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events']


def add_concert_to_events(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_args = ['concert_id', 'token']

    if not check_keys_in_dict(request, approved_args):
        raise ValueError('Incorrect input data')

    user = db.session.query(User) \
        .filter(User.user_token == request['token']) \
        .first()

    concert = db.session.query(Concert) \
        .get(int(request['concert_id']))

    if not concert:
        raise ValueError("concert not found")

    if not user:
        raise ValueError(TOKEN_NOT_FOUND)

    if not user.user_google_access_token:
        raise ValueError("google token not found")

    with open('credentials.json', 'r') as json1_file:
        json1_str = json1_file.read()
        cred_data = json.loads(json1_str)['web']

        cred_data['token'] = user.user_google_access_token
        cred_data['refresh_token'] = user.user_google_access_token
        cred_data['expiry'] = user.user_google_token_exp_date.isoformat()

    creds = Credentials.from_authorized_user_info(cred_data, scopes=scopes)

    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                user.user_google_access_token = creds.token
                user.user_google_refresh_token = creds.refresh_token
                user.user_google_token_exp_date = creds.expiry.isoformat()
                db.session.commit()
    except RefreshError:
        return recreate_token_for_response({SUCCESS_KEY: False,
                                            DESCRIPTION_KEY: "can't refresh token"})

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': str(concert.concert_name),
        'location': str(concert.hall.hall_name),
        'start': {
            'dateTime': str(concert.concert_date.isoformat()),
            'timeZone': 'Europe/Moscow'
        },
        'end': {
            'dateTime': (concert.concert_date + timedelta(hours=1)).isoformat(),
            'timeZone': 'Europe/Moscow'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return recreate_token_for_response({SUCCESS_KEY: True},
                                       request['token'])
