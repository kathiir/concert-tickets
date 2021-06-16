from typing import Any, Dict

import google_auth_oauthlib.flow

GOOGLE_OAUTH2_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_OAUTH2_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
USERINFO_PROFILE_SCOPE = 'https://www.googleapis.com/auth/userinfo.profile'

scopes = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events']


# stateless version (I NEED ONLY URL)
def get_google_auth_url_stateless(redirect_uri: str) -> str:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", scopes=scopes)

    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    return authorization_url


# stateful
def get_google_auth_url_stateful(redirect_uri: str, state: str) -> (str, str):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", scopes=scopes)

    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        state=state,
        include_granted_scopes='true')

    return authorization_url, state


# stateless
def get_google_credentials_stateless(flask_request_url: str, redirect_uri: str):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json.json',
        scopes=scopes)

    flow.redirect_uri = redirect_uri
    authorization_response = flask_request_url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    result = {'google_access_token': credentials.token,
              'google_refresh_token': credentials.refresh_token}

    return result


# stateful
def get_google_credentials_stateful(flask_request_url: str, redirect_uri: str, state: str) -> Dict[str, Any]:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=scopes,
        state=state)

    flow.redirect_uri = redirect_uri
    authorization_response = flask_request_url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    result = {'google_access_token': credentials.token,
              'google_refresh_token': credentials.refresh_token}

    return result