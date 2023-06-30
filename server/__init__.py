from flask import Flask, render_template
from .views import account, index, edit, serve
from flask_cors import CORS


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(SECRET_KEY='dev')

    app.register_blueprint(serve.blueprint)
    app.register_blueprint(account.blueprint)
    app.register_blueprint(index.blueprint)
    app.register_blueprint(edit.blueprint)

   # Catch all requests that doesn't start with /api
   # If route not found, then return 404

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if not path.startswith('api/'):
            return render_template("index.html")
        else:
            return 'Page not found', 404

    return app
