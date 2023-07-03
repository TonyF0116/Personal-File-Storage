from flask import Blueprint, jsonify, request


# Handle requests from the account page
blueprint = Blueprint('account', __name__, url_prefix='/api/account')


@blueprint.route('/login', methods=['POST'])
def login():
    """
    Handles login requests
    ---
    tags:
      - Account
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: User entered username.
      - name: password
        in: formData
        type: string
        required: true
        description: User entered password.
    responses:
      200:
        description: OK
      401:
        description: Incorrect credentials
    """
    username = request.form.get('username')
    password = request.form.get('password')
    return {'code': 200,
            'msg': None,
            'data': None}
