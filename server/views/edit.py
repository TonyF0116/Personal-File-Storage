from flask import Blueprint


# Handle requests from the edit page
blueprint = Blueprint('edit', __name__, url_prefix='/api/edit')
