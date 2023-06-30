from flask import Blueprint, send_from_directory, send_file


# Handle requests for serving static files
blueprint = Blueprint('serve', __name__)


# Send requested css files
@blueprint.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('templates/css', path)


# Send requested js files
@blueprint.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('templates/js', path)


@blueprint.route('/favicon.ico')
def serve_favicon():
    return send_file('templates/favicon.ico')
