from flask import Blueprint, url_for, request, send_file
from ..utils.jwt_validation import jwt_validation
from ..models.edit import get_file_info
import pandas as pd

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


# Route for updating excel files
@blueprint.route('/save_excel', methods=['POST'])
def save_excel():
    # Retrieve the file id and updated data from the request
    excel_data = request.get_json()
    file_id = request.args.get('file_id')

    # Get belonging and file name from the database
    file_info = get_file_info(file_id)
    account_id = file_info[0][0]
    file_name = file_info[0][1]

    # Construct file path
    file_path = 'server/files/{}/{}'.format(account_id, file_name)

    # Do the update
    try:
        df = pd.read_excel(file_path, header=None)
        max_rows = max(len(df), len(excel_data))
        max_cols = max(len(df.columns), max(len(row) for row in excel_data))
        df = df.reindex(index=range(max_rows), columns=range(max_cols))

        for row_index, row in enumerate(excel_data):
            for cell_index, value in enumerate(row):
                df.iat[row_index, cell_index] = value

        df.to_excel(file_path, header=False, index=False)

        return {'msg': 'Save successful',
                'data': None}, 200

    except Exception as error:
        print(error)
        return {'msg': 'Save Failed. Check server terminal for more info.',
                'data': None}, 500
