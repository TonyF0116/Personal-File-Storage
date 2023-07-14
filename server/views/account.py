from flask import Blueprint, request, url_for, current_app, make_response
from ..models.account import sign_up, check_username_num, check_password, update_user_info
from ..config import jwt_key
import jwt
from datetime import datetime, timedelta, timezone
from ..utils.jwt_validation import jwt_validation
from os import path, mkdir
import base64
from ..models.index import add_new_file

# Handle requests from the account page
blueprint = Blueprint('account', __name__, url_prefix='/api/account')


# Handles account page redirecting JWT authorization validation
@blueprint.route('', methods=['POST'])
def account():
    # Retrieve the token and redirection from request header and url
    # Return unauthorized if Authorization not in header or cookies
    authorization = request.headers.get('Authorization')
    redirection = request.args.get('redirection')
    if authorization == None:
        if request.cookies.get('token') != None:
            authorization = request.cookies.get('token')
        else:
            return {'msg': "Unauthorized",
                    'data': {'redirection': redirection}}, 401
    token = authorization[7:]

    # Validate the token and authorization
    result = jwt_validation(token, redirection)

    # If authorized, do the redirection
    if result['msg'] == 'Authorized':
        return {'msg': 'Authorized',
                'data': {'redirection': redirection,
                         'token': 'Bearer {}'.format(token)}}, 200
    # If unauthorized but validation succeeded, grant the permission and do the redirection
    if result['msg'] == 'Unauthorized':
        token_info = result['data']['payload']
        if 'index' in redirection:
            token_info['index_page_authorization'] = True
        if 'edit' in redirection:
            token_info['edit_page_authorization'] = True

        token = jwt.encode(payload=token_info, key=jwt_key, algorithm="HS256")
        # Store token in cookie
        response = make_response({'msg': "Authorized",
                                  'data': {'redirection': redirection+'?file_id='+request.args.get('file_id'),
                                           'token': 'Bearer {}'.format(token)}})
        response.set_cookie('token', 'Bearer {}'.format(token))

        return response, 200

    return {'msg': "Unauthorized",
            'data': {'redirection': redirection}}, 401


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
        "index_page_authorization": True,
        "edit_page_authorization": False
    }
    token = jwt.encode(payload=token_info, key=jwt_key, algorithm="HS256")

    current_app.redis_conn.sadd('online_users', token)

    # Store token in cookie
    response = make_response({'msg': "Sign up successful",
                              'data': {"account_id": user[0][0],
                                       'token': 'Bearer {}'.format(token)}})
    response.set_cookie('token', 'Bearer {}'.format(token))

    return response, 200


@blueprint.route('/login', methods=['POST'])
def login():
    # Parse the input username, password_hash, and redirection from the request form and url
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')
    redirection = request.args.get('redirection')

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
    # Redirect to index page if redirection not provided
    if redirection == None:
        redirection = url_for('route_index')
    if 'index' in redirection:
        token_info['index_page_authorization'] = True
    if 'edit' in redirection:
        token_info['edit_page_authorization'] = True

    token = jwt.encode(payload=token_info, key=jwt_key, algorithm="HS256")

    current_app.redis_conn.sadd('online_users', token)

    # Store token in cookie
    response = make_response({'msg': "Login successful",
                              'data': {'redirection': redirection,
                                       'token': 'Bearer {}'.format(token)}})
    response.set_cookie('token', 'Bearer {}'.format(token))

    return response, 200


# Update user nickname and avatar suffix
@blueprint.route('/new_user_info', methods=['POST'])
def new_user_info():
    # Retrieve data from the form
    avatar_data = request.form.get('avatar')
    avatar_name = request.form.get('avatar_name')
    nickname = request.form.get('nickname')
    account_id = request.form.get('account_id')

    # Split the avatar suffix
    avatar_suffix = avatar_name.split('.')[-1]
    avatar_name = 'avatar.{}'.format(avatar_suffix)

    try:

        # Save the avatar in the user's files folder
        avatar = base64.b64decode(avatar_data)

        if not path.exists('server/files/{}/'.format(account_id)):
            mkdir('server/files/{}/'.format(account_id))

        with open(path.join('server/files/{}/{}'.format(account_id, avatar_name)), 'wb') as f:
            f.write(avatar)

        # Update info in the database
        update_user_info(account_id, nickname, avatar_suffix)
        add_new_file(account_id, avatar_name, 0,
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return {'msg': 'Success',
                'data': None}, 200

    except Exception as error:
        print(error)
        return {'msg': 'Unknown error. Check server terminal for more info.',
                'data': {'error': str(error)}}, 500


# Route for getting all logged in user info
@blueprint.route('get_logged_in_users', methods=['POST'])
def get_logged_in_users():
    logged_in_users = current_app.redis_conn.smembers('online_users')
    result = ''
    for user in logged_in_users:
        validation = jwt_validation(user.decode('utf-8'), '/account')
        if validation['msg'] == 'Validation failed':
            current_app.redis_conn.srem('online_users', user)
        else:
            payload = validation['data']['payload']
            result += 'Account_id: {}; Login_time: {}; Expire: {}\n'.format(
                payload['account_id'], datetime.fromtimestamp(
                    payload['nbf']).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(payload['exp']).strftime('%Y-%m-%d %H:%M:%S'))
    return {'msg': None,
            'data': {'users': result}}, 200


# Routes for handling logout request
@blueprint.route('logout', methods=['POST'])
def logout():
    response = make_response({'msg': 'Logout successful',
                              'data': None})
    # Clear token in cookie
    response.set_cookie('token', '')
    return response, 200
