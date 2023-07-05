from flask import Flask, render_template, request
from .views import account, index, edit, serve
from flask_cors import CORS
from flasgger import Swagger


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SWAGGER'] = {'openapi': '3.0.0'}
    swagger = Swagger(app, template_file='swagger_config.yaml')

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
        main_pages = ['', 'index', 'index/',
                      'account', 'account/', 'edit', 'edit/']
        if path in main_pages:
            return render_template("index.html")
        else:
            return {'msg': 'Page Not Found',
                    'data': None}, 404

    return app
