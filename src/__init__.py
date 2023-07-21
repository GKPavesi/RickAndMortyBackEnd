from flask import Flask, jsonify
from src.database import db, ma
from src.search import search
from src.utils.exception_tracker_log import log_exception
from src.constants.http_status_codes import *
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(search)

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
