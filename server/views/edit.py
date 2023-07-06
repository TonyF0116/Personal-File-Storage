from flask import Blueprint, url_for, request
from ..utils.jwt_validation import jwt_validation

# Handle requests from the edit page
blueprint = Blueprint('edit', __name__, url_prefix='/api/edit')


@blueprint.route('', methods=['POST'])
def edit():
    # Retrieve the token from request header
    # Return redirection if Authorization not in header
    authorization = request.headers.get('Authorization')
    if authorization == None:
        return {'msg': 'Validation failed',
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_edit'))}}, 401

    # Decode the JWT token
    token = authorization[7:]
    result = jwt_validation(token, url_for('route_edit'))

    # Validation failed => Invalid token => Login again
    if result['msg'] == 'Validation failed':
        return {'msg': 'Validation failed',
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_edit'))}}, 401

    # Unauthorized => Valid token with no auth => Go to account page to get authorization
    if result['msg'] == 'Unauthorized':
        return {'msg': "Unauthorized",
                'data': {'redirection': '{}?redirection={}&Authorization={}'
                         .format(url_for('route_account'), url_for('route_edit'), authorization)}}, 302

    account_id = result['data']['payload']['account_id']

    return {'msg': None,
            'data': {'account_id': account_id}}, 200
