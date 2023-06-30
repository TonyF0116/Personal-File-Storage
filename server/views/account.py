from flask import Blueprint


# Handle requests from the account page
blueprint = Blueprint('account', __name__, url_prefix='/api/account')
