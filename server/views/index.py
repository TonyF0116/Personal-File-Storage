from flask import Blueprint


# Handle requests from the index page
blueprint = Blueprint('index', __name__, url_prefix='/api/index')
