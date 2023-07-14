from flask import Flask, render_template, request
from .views import account, index, edit, serve
from flask_cors import CORS
from flasgger import Swagger
from os import path, mkdir
import logging
import json


def create_app():
    if not path.exists('server/files/'):
        mkdir('server/files/')

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SWAGGER'] = {'openapi': '3.0.0'}
    swagger = Swagger(app, template_file='swagger_config.yaml')

    app.config.from_mapping(SECRET_KEY='dev')

    # Configuration for logging
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('server.log')
    file_handler.setFormatter(log_formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    @app.before_request
    def log_request():
        if not (request.path.startswith('/js') or request.path.startswith('/css')
                or request.path.startswith('/avatar') or request.path.startswith('/favicon.ico')):
            log_message = f"[{request.method}] {request.url}\n"
            log_message += f"Authorization header: {request.headers.get('Authorization')}\n"
            log_message += f"Cookie token: {request.cookies.get('token')}"
            if request.form:
                log_message += f"\nForm Data: {request.form}"

            app.logger.info(log_message)

    @app.after_request
    def log_response(response):
        if not (request.path.startswith('/js') or request.path.startswith('/css')
                or request.path.startswith('/avatar') or request.path.startswith('/favicon.ico')):
            log_message = f"Response: {response.status} {json.dumps(response.json)}\n"
            app.logger.info(log_message)
        return response

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
