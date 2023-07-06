from flask import Blueprint, request, url_for
from ..models.index import get_user_info, get_user_files
from ..utils.jwt_validation import jwt_validation

# Handle requests from the index page
blueprint = Blueprint('index', __name__, url_prefix='/api/index')


# Route for validating authorization and get basic user information
@blueprint.route('', methods=['POST'])
def index():
    # Retrieve the token from request header
    # Return redirection if Authorization not in header
    authorization = request.headers.get('Authorization')
    if authorization == None:
        return {'msg': 'Validation failed',
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_index'))}}, 401

    # Decode the JWT token
    token = authorization[7:]
    result = jwt_validation(token, url_for('route_index'))

    # Validation failed => Invalid token => Login again
    if result['msg'] == 'Validation failed':
        return {'msg': "Unauthorized",
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_index'))}}, 401

    # Unauthorized => Valid token with no auth => Go to account page to get authorization
    if result['msg'] == 'Unauthorized':
        return {'msg': "Unauthorized",
                'data': {'redirection': '{}?redirection={}&Authorization={}'
                         .format(url_for('route_account'), url_for('route_index'), authorization)}}, 302

    # Retrieve account_id and other user basic information
    account_id = result['data']['payload']['account_id']
    user_info = get_user_info(account_id)
    user_files = get_user_files(account_id)
    # print(user_info)
    # print(user_files)
    return {'msg': None,
            'data': {'account_id': account_id}}, 200
