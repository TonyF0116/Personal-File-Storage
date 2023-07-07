from flask import Blueprint, send_from_directory, send_file, request


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


# Send requested favicon files
@blueprint.route('/favicon.ico')
def serve_favicon():
    return send_file('templates/favicon.ico')


# Send requested avatar
@blueprint.route('/avatar')
def serve_avatar():
    account_id = request.args.get('account_id')
    suffix = request.args.get('suffix')
    if suffix == 'suffix':
        return 'Not found', 404
    return send_file('files/{}/avatar.{}'.format(account_id, suffix))
