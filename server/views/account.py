from flask import Blueprint, request, url_for, make_response
from ..models.account import sign_up, check_username_num, check_password
from ..config import key
import jwt
from datetime import datetime, timedelta, timezone

# Handle requests from the account page
blueprint = Blueprint('account', __name__, url_prefix='/api/account')


@blueprint.route('/')
def account():
    # Check current token in cookie
    print(request.headers)
    token = request.cookies

    # If token exist, decode the token
    if token != None:
        try:
            jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        # If successfully decoded, redirect back with the token added as a arg
        except jwt.ExpiredSignatureError:
            pass
        except jwt.DecodeError:
            pass
        else:
            return 'a'
            # return make_response(request.args.get('redirect')+'?token={}'.format(token))
    return 'b'


@blueprint.route('/signup', methods=['POST'])
def signup():
    # Parse the input username, password_hash, and redirection from the request form
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')

    # If the number of users with the given username is not 0,
    # then this is a duplicated username, return the error msg
    if check_username_num(username) != 0:
        return "Username already existed."

    # Sign up using the given username and password
    user = sign_up(username, password_hash)

    # Sign up successful, build JWT token
    token_info = {
        "account_id": user[0][0],
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "nbf": datetime.now(tz=timezone.utc),
        "account_page_authorization": True,
        "index_page_authorization": False,
        "edit_page_authorization": False
    }
    token = jwt.encode(payload=token_info, key=key, algorithm="HS256")

    # Make response with the redirection info
    response = make_response({'msg': None,
                              'data': {'url': url_for('catch_all')+'?token={}&new_user=true'.format(token)}})

    # Set cookie for account page
    response.set_cookie(key='token', value=token, path='/account')
    return response, 302


@blueprint.route('/login', methods=['POST'])
def login():
    # Parse the input username, password_hash, and redirection from the request form
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')
    redirection = request.form.get('redirection')

    print(request.headers)

    # If the number of users with the given username is not 1,
    # then there is an no such user in the database, return the error msg
    if check_username_num(username) != 1:
        return {'msg': "Username doesn't exist.",
                'data': None}, 401

    # Login using the given username and password
    login_user = check_password(username, password_hash)

    # If matched user found is not 1, then the input doesn't match, return the error msg
    if len(login_user) != 1:
        return {'msg': "Incorrect password",
                'data': None}, 401

    # Login successful, build JWT token
    token_info = {
        "account_id": login_user[0][0],
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "nbf": datetime.now(tz=timezone.utc),
        "account_page_authorization": True,
        "index_page_authorization": False,
        "edit_page_authorization": False
    }
    token = jwt.encode(payload=token_info, key=key, algorithm="HS256")

    # Redirect to index page if redirection not provided
    if redirection == None:
        redirection = url_for('catch_all')

    # Make response with the redirection info
    response = make_response({'msg': None,
                              'data': {'url': redirection+'?token={}'.format(token)}})

    # Set cookie for account page
    response.set_cookie(key='token', value=token, path='/account')
    return response, 302
