from flask import Blueprint, request, url_for
from ..models.index import get_user_info, get_user_files, add_new_file
from ..utils.jwt_validation import jwt_validation
from datetime import datetime
from os import path, mkdir

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
        return {'msg': 'Validation failed',
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
    return {'msg': None,
            'data': {'user_info': user_info,
                     'user_files': user_files}}, 200


# Route for uploading new files
@blueprint.route('/upload_file', methods=['POST'])
def upload_file():
    # Get account_id and file from formData
    account_id = request.form['account_id']
    file = request.files['file']
    file_name = file.filename

    # Save file on server
    # Return error message if failed
    if not path.exists('server/files/{}/'.format(account_id)):
        mkdir('server/files/{}/'.format(account_id))
    try:
        file.save('server/files/{}/{}'.format(account_id, file_name))
    except Exception as error:
        print(error)
        return {'msg': 'Save file failed. Check server terminal for more info.',
                'data': None}, 500

    # Retrieve file_suffix and decide file_type
    file_suffix = file_name.split('.')[-1]
    if file_suffix in ['jpg', 'jpeg', 'png']:
        file_type = 0
    elif file_suffix == 'pdf':
        file_type = 1
    else:
        file_type = 2

    # Format current time
    last_modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Update in databse
    add_new_file(account_id, file_name, file_type, last_modified)

    return {'msg': 'File uploaded successfully.',
            'data': None}, 200
