from flask import Flask, jsonify
from src.database import db, ma
from src.search import search
from src.authentication import authentication
from src.utils.exception_tracker_log import log_exception
from src.constants.http_status_codes import *
from dotenv import load_dotenv
from src.extensions.cache import cache
from flasgger import Swagger
from src.config.swagger import template, swagger_config
from flask_cors import CORS
from src.firebase.auth import firebase
import os

load_dotenv()

def create_app():

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,

        SWAGGER = {
            'title': 'Rick And Morty Backend Api',
            'uiversion': 3
        }
    )

    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

    app.register_blueprint(search)
    app.register_blueprint(authentication)

    Swagger(app, config = swagger_config, template = template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'page not found'}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(Exception)
    def handle_exceptions(e):
        log_exception(e)
        return jsonify({
            'success': False,
            'error': 'Something bad happened, please try again'
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app
