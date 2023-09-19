from flask import Blueprint, jsonify, request
from src.database import Users, user_schema, db
from src.constants.http_status_codes import *
from firebase_admin import auth, exceptions
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

authentication = Blueprint('authentication', __name__, url_prefix='/auth')

@authentication.post('/register')
def handle_registration():
    try:
        data = request.get_json()

        validated_data = user_schema.load(data)

        firebaseUser = auth.get_user(validated_data.get('firebase_uid'))

        if firebaseUser.email.strip() != validated_data.get('email').strip():
            raise exceptions.FirebaseError('INVALID_ARGUMENT', 'INVALID_ARGUMENT')

        user = Users(firebase_uid = validated_data.get('firebase_uid'),
                     first_name = validated_data.get('first_name'),
                     last_name = validated_data.get('last_name'),
                     email = validated_data.get('email')
                     )
        
        db.session.add(user)
        db.session.commit()

        user = user_schema.dump(user)

        return jsonify({
            'success': True,
            'user': user
        }), HTTP_201_CREATED
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'user': None
        }), HTTP_400_BAD_REQUEST
    
    except exceptions.FirebaseError as e:
        return jsonify({
            'success': False,
            'user': None
        }), HTTP_400_BAD_REQUEST
    
    except SQLAlchemyError as e:
        db.session.rollback()
        raise

    except Exception as e:
        raise

@authentication.post('/info')
def return_user_info():
    try:

        auth_header = request.headers.get('Authorization')

        data = request.get_json()

        request_firebase_uid = data.get('firebase_uid')

        if auth_header and request_firebase_uid:

            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

                decoded_token = auth.verify_id_token(token)

                token_firebase_uid = decoded_token['uid']

                if (token_firebase_uid != request_firebase_uid):
                    return jsonify({
                    'success': False,
                    'user': None,
                    'message': 'Invalid user and token'
                }), HTTP_400_BAD_REQUEST

                user = Users.query.filter(Users.firebase_uid == token_firebase_uid).first_or_404()

                user = user_schema.dump(user)

                return jsonify({
                    'success': True,
                    'user': user
                }), HTTP_200_OK
            
            else:
                return jsonify({
                'success': False,
                'user': None,
                'message': 'Invalid authentication header'
            }), HTTP_401_UNAUTHORIZED
        else:
            return jsonify({
                'success': False,
                'user': None,
                'message': 'No authentication header or firebase uid provided'
            }), HTTP_401_UNAUTHORIZED
        
    except exceptions.FirebaseError as e:
        return jsonify({
            'success': False,
            'user': None,
            'message': e.default_message
        }), HTTP_400_BAD_REQUEST

    except NotFound as e:
        return jsonify({
            'success': False,
            'error': 'Something bad happened, please try again'
        }), HTTP_404_NOT_FOUND

    except SQLAlchemyError as e:
        db.session.rollback()
        raise
        
    except Exception as e:
        raise