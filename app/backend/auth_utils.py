import hashlib
import random
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from sqlalchemy import or_
from validate_email import validate_email

from const_keys import SUCCESS_KEY, DESCRIPTION_KEY, TOKEN_NOT_FOUND
from models import User
from models import db
from utils import check_keys_in_dict


def registration_check(input: Dict[str, Any]) -> Dict[str, Any]:
    result = dict()
    is_correct = "nickname" in input \
           and "email" in input \
           and "password" in input \
           and "password_check" in input

    if not is_correct:
        result['success'] = False
        return result

    if not validate_email(input['email']):
        is_correct = False
        result['email'] = 'Incorrect email address'

    if db.session.query(User).filter(User.user_email == input['email']).first():
        is_correct = False
        result['email'] = 'This email already exists'

    if db.session.query(User).filter(User.username == input['nickname']).first():
        is_correct = False
        result['nickname'] = 'This nickname already exists'

    if input["password_check"] != input["password"]:
        is_correct = False
        result['password_check'] = 'Passwords don\'t match'

    if len(input["password"]) < 8:
        is_correct = False
        result['password'] = 'Password length must be greater than 7'

    if is_correct:
        result['success'] = True
    else:
        result['success'] = False

    return result


def register_user_with_response(input: Dict[str, Any]) -> Dict[str, Any]:
    response = registration_check(input)
    if not response['success']:
        return response

    user = User()
    user.user_email = input['email']
    user.username = input['nickname']
    user.user_role = 0
    user.user_password = hash_password(input['password'])
    user.user_token = create_user_token()
    user.user_token_exp_date = datetime.now() + timedelta(days=1)
    db.session.add(user)
    db.session.commit()

    response['token'] = user.user_token
    return response


def change_passwd(request: Dict[str, Any]) -> Dict[str, Any]:
    approved_keys = ['token', 'old_password', 'new_password']

    if not check_keys_in_dict(request, approved_keys):
        raise ValueError("not approved key")

    if len(request['new_password']) < 8:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: "Password length must be greater than 7"}

    user = db.session\
        .query(User)\
        .filter(User.user_token == request['token'])\
        .first()

    if not user:
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: TOKEN_NOT_FOUND}

    if not check_pass(request['old_password'], user.user_password):
        return {SUCCESS_KEY: False, DESCRIPTION_KEY: "wrong old password"}

    user.user_password = hash_password(request['new_password'])
    db.session.commit()

    return recreate_token_for_response({SUCCESS_KEY: True}, request['token'])


def create_user_token() -> str:
    return secrets.token_hex(32)


def login_user_by_login_and_pass(user_login: str, passwd: str) -> Dict[str, Any]:
    response = dict()
    user = db.session.query(User) \
        .filter(or_(user_login == User.user_email, user_login == User.username)) \
        .first()

    if not user \
            or not check_pass(passwd, user.user_password) \
            or user.user_role == 1:

        response['success'] = False
        response['description'] = 'incorrect login or pass'
        return response

    token = create_user_token()
    user.user_token = token
    user.user_token_exp_date = datetime.now() + timedelta(days=1)
    db.session.add(user)
    db.session.commit()

    response['success'] = True
    response['token'] = token
    return response


def recreate_user_token(last_token: str) -> str:
    user = db.session.query(User)\
        .filter(User.user_token == last_token)\
        .first()

    if user and user.user_role == 1:
        return ""

    if user and user.user_token_exp_date <= datetime.now():
        user.user_token = create_user_token()
        user.user_token_exp_date = datetime.now() + timedelta(days=1)
        db.session.add(user)
        db.session.commit()
        return user.user_token

    return ""


def recreate_token_for_response(response: Dict[str, Any], token: str) -> Dict[str, Any]:
    if a := recreate_user_token(token):
        response['token'] = a

    return response


def check_pass(passwd: str, passwd_with_hash: str) -> bool:
    passwd_hash = passwd_with_hash.split('@', 2)[0]
    salt = passwd_with_hash.split('@', 2)[1]

    if hash_password_using_salt(passwd, salt) == passwd_hash:
        return True

    return False


def hash_password(passwd: str) -> str:
    if len(passwd) < 8:
        raise ValueError("Password length must be greater than 7")  # incorrect passwd length

    random.seed(passwd)
    salt = secrets.token_hex(16)

    result_hash = hash_password_using_salt(passwd, salt) \
                  + "@" + salt
    return result_hash


def hash_password_using_salt(passwd: str, salt: str):
    assert len(salt) == 32
    assert len(passwd) > 7

    passwd_len = len(passwd)
    passwd_with_salt = salt[:4] \
                       + passwd[:int(passwd_len / 2)] \
                       + salt[4: 12] \
                       + passwd[-int(passwd_len / 2 + passwd_len % 2):] \
                       + salt[-4:]

    return hashlib.sha256(passwd_with_salt.encode()).hexdigest()
