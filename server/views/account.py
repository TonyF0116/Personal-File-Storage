from flask import Blueprint, request, url_for, make_response
from ..models.account import sign_up, check_username_num, check_password
from ..config import key
import jwt
from datetime import datetime, timedelta, timezone
from ..utils.jwt_validation import jwt_validation

# Handle requests from the account page
blueprint = Blueprint('account', __name__, url_prefix='/api/account')


@blueprint.route('/')
def account():
    # Retrieve the token and redirection from request header and url
    token = request.headers.get('Authorization')[7:]
    redirection = request.args.get('redirection')

    # Validate the token and authorization
    result = jwt_validation(token, redirection)

    # If authorized, do the redirection
    if result['msg'] == 'Authorized':
        return {'msg': 'Authorized',
                'data': {'url': redirection}}, 302
    # If unauthorized but validation succeeded, grant the permission and do the redirection
    if result['msg'] == 'Unauthorized':
        token_info = result['data']['payload']
        if 'index' in redirection:
            token_info['index_page_authorization'] = True
        if 'edit' in redirection:
            token_info['edit_page_authorization'] = True

        token = jwt.encode(payload=token_info, key=key, algorithm="HS256")

        # Make response with the redirection info
        response = make_response({'msg': "Authorized",
                                  'data': {'url': redirection}})

        # Set the Authorization header
        response.headers['Authorization'] = 'Bearer {}'.format(token)
        return response, 302

    return {'msg': "Unauthorized",
            'data': {'url': redirection}}, 401


@blueprint.route('/signup', methods=['POST'])
def signup():
    # Parse the input username, password_hash, and redirection from the request form
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')

    # If the number of users with the given username is not 0,
    # then this is a duplicated username, return the error msg
    if check_username_num(username) != 0:
        return {'msg': "Username already existed.",
                'data': None}, 400

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
    response = make_response({'msg': "Sign up successful",
                              'data': {'url': url_for('route_account')+'?new_user=true'}})

    # Set the Authorization header
    response.headers['Authorization'] = 'Bearer {}'.format(token)
    return response, 302


@blueprint.route('/login', methods=['POST'])
def login():
    # Parse the input username, password_hash, and redirection from the request form
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')
    redirection = request.form.get('redirection')

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
        redirection = url_for('route_index')

    # Make response with the redirection info
    response = make_response({'msg': None,
                              'data': {'url': redirection}})

    # Set the Authorization header
    response.headers['Authorization'] = 'Bearer {}'.format(token)
    return response, 302
