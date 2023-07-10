from flask import Flask, render_template, request
from .views import account, index, edit, serve
from flask_cors import CORS
from flasgger import Swagger
from os import path, mkdir


def create_app():
    if not path.exists('server/files/'):
        mkdir('server/files/')

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SWAGGER'] = {'openapi': '3.0.0'}
    swagger = Swagger(app, template_file='swagger_config.yaml')

    app.config.from_mapping(SECRET_KEY='dev')

    app.register_blueprint(serve.blueprint)
    app.register_blueprint(account.blueprint)
    app.register_blueprint(index.blueprint)
    app.register_blueprint(edit.blueprint)

    # Routes for the main pages

    @app.route('/')
    def route_empty():
        return render_template("index.html")

    @app.route('/index')
    def route_index():
        return render_template("index.html")

    @app.route('/account')
    def route_account():
        return render_template("index.html")

    @app.route('/edit')
    def route_edit():
        return render_template("index.html")

    return app
