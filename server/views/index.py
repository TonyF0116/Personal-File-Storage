from flask import Blueprint, request, url_for, send_file
from ..models.index import get_user_info, get_user_files, add_new_file, check_belonging, delete_file
from ..utils.jwt_validation import jwt_validation
from datetime import datetime
from os import path, mkdir, remove
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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


# Route for serveing download requested files
@blueprint.route('/download')
def download():
    # Retrieve the authorization token and file_id from request args
    authorization = request.args.get('Authorization')
    file_id = request.args.get('file_id')

    # Decode the JWT token
    token = authorization[7:]
    result = jwt_validation(token, url_for('route_index'))

    # Validation failed => Invalid token => Login again
    if result['msg'] == 'Validation failed':
        return {'msg': 'Validation failed',
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_index'))}}, 401

    # Retrieve account_id and check belonging
    account_id = result['data']['payload']['account_id']
    result = check_belonging(account_id, file_id)
    if len(result) == 1:
        return send_file('files/{}/{}'.format(account_id, result[0][0]))
    else:
        return {'msg': "Unauthorized",
                'data': None}, 401


# Route for generating file stat
@blueprint.route('/file_stat_generation', methods=['POST'])
def file_stat_generation():
    try:
        # Get account_id from request args and user files
        account_id = request.args.get('account_id')
        data = get_user_files(account_id)

        # Generate new file
        doc = SimpleDocTemplate(
            "server/files/{}/file_stat.pdf".format(account_id), pagesize=letter)

        elements = []
        title = "File Stat"
        styles = getSampleStyleSheet()
        title_text = Paragraph(title, styles['Title'])
        elements.append(title_text)

        # Update in database
        add_new_file(account_id, 'file_stat.pdf', 1,
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data = get_user_files(account_id)

        # Headaers
        table_data = [['File Id', 'File Name', 'File Type', 'Last Modified']]
        for item in data:
            row = [item[0], item[2], item[3], item[4]]
            table_data.append(row)

        # Render the file
        table = Table(table_data)
        table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTSIZE', (0, 0), (-1, 0), 12),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ]))
        elements.append(table)
        doc.build(elements)

        return {'msg': 'Generated Successfully.',
                'data': None}, 200
    except Exception as error:
        print(error)
        return {'msg': 'Generated Failed. Check server terminal for more info.',
                'data': None}, 500


# Route for deleting a file
@blueprint.route('/delete', methods=['DELETE'])
def delete():
    # Retrieve the authorization token and file_id from request args
    authorization = request.args.get('Authorization')
    file_id = request.args.get('file_id')

    # Decode the JWT token
    token = authorization[7:]
    result = jwt_validation(token, url_for('route_index'))

    # Validation failed => Invalid token => Login again
    if result['msg'] == 'Validation failed':
        return {'msg': 'Validation failed',
                'data': {'redirection': '{}?redirection={}&warning=Login+Expired'
                         .format(url_for('route_account'), url_for('route_index'))}}, 401

    # Retrieve account_id and check belonging
    account_id = result['data']['payload']['account_id']
    result = check_belonging(account_id, file_id)
    if len(result) == 1:
        remove('server/files/{}/{}'.format(account_id, result[0][0]))
        delete_file(file_id)
        return {'msg': "Deleted",
                'data': None}, 200
    else:
        return {'msg': "Unauthorized",
                'data': None}, 401


# Route for creating new excel file
@blueprint.route('/new_excel_file', methods=['POST'])
def new_excel_file():
    # Get account_id and file name from request args
    account_id = request.args.get('account_id')
    file_name = request.args.get('file_name')

    # Try create a new excel file
    if not path.exists('server/files/{}/'.format(account_id)):
        mkdir('server/files/{}/'.format(account_id))
    try:
        df = pd.DataFrame([[]])
        df.to_excel('server/files/{}/{}.xlsx'.format(account_id,
                    file_name), header=False, index=False)
    except Exception as error:
        print(error)
        return {'msg': 'Create file failed. Check server terminal for more info.',
                'data': None}, 500

    # Update in databse
    add_new_file(account_id, '{}.xlsx'.format(file_name), 2,
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return {'msg': 'File created successfully.',
            'data': None}, 200
