from flask import Blueprint, url_for, request, send_file
from ..utils.jwt_validation import jwt_validation
from ..models.edit import get_file_info

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
                'data': {'redirection': '{}?redirection={}&file_id={}&Authorization={}'
                         .format(url_for('route_account'), url_for('route_edit'), request.args.get('file_id'), authorization)}}, 302

    account_id = result['data']['payload']['account_id']

    # Retrieve file type and build return info
    file_id = request.args.get('file_id')
    file_type = get_file_info(file_id)[0][2]

    return {'msg': None,
            'data': {'account_id': account_id,
                     'file_type': file_type}}, 200


# Routes for serving files for the edit page
@blueprint.route('/get_file')
def get_file():
    # Retrieve info from the args
    account_id = request.args.get('account_id')
    file_id = request.args.get('file_id')

    # If file id not given, return warning png
    if file_id == 'undefined':
        return send_file('files/Unauthorized.png')

    file_info = get_file_info(file_id)

    # Check belonging
    if int(file_info[0][0]) != int(account_id):
        if file_info[0][2] == 0:
            return send_file('files/Unauthorized.png')
        elif file_info[0][2] == 1:
            return send_file('files/Unauthorized.pdf')
        else:
            pass
    else:
        return send_file('files/{}/{}'.format(file_info[0][0], file_info[0][1]))
