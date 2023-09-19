from functools import wraps
from flask import request, jsonify
from firebase_admin import auth
from src.constants.http_status_codes import *

def authenticate_with_firebase_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:

            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return jsonify({
                    'success': False,
                    'user': None,
                    'message': 'No authentication header or firebase uid provided'
                }), HTTP_401_UNAUTHORIZED

            if not auth_header.startswith('Bearer '):
                return jsonify({
                    'success': False,
                    'user': None,
                    'message': 'Invalid authentication header'
                }), HTTP_401_UNAUTHORIZED

            token = auth_header.split(' ')[1]

            decoded_token = auth.verify_id_token(token)

            return f(*args, **kwargs)

        except auth.InvalidIdTokenError:
            return jsonify({
                'success': False,
                'user': None,
                'message': 'Invalid authentication token'
            }), HTTP_401_UNAUTHORIZED

        except Exception as e:
            return jsonify({
                'success': False,
                'user': None,
                'message': str(e)
            }), HTTP_400_BAD_REQUEST

    return decorated_function