from flask import Blueprint, jsonify, request
from src.database import Characters, character_schema, characters_schema
from sqlalchemy import asc
from src.constants.http_status_codes import *
import math

search = Blueprint('search', __name__, url_prefix='/search')

@search.get('/')
@search.get('/<int:character_id>')
def handle_search(character_id=None):
    try:
        if character_id is not None:
            character = Characters.query.get(character_id)
            if not character:
                return jsonify({
                    'success': False,
                    'error': 'Character not found'
                }), HTTP_404_NOT_FOUND

            character_data = character_schema.dump(character)
            return jsonify({
                'success': True,
                'character': character_data
            }), HTTP_200_OK
        else:
            name = request.args.get('name')
            page = request.args.get('page', 1)

            try:
                page = int(page)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid page number. Please enter a valid integer.'
                }), HTTP_400_BAD_REQUEST

            character_count = Characters.query.filter(Characters.name.ilike(f"%{name}%")).count()

            if not character_count:
                return jsonify({
                    'success': False,
                    'error': 'No characters found with the given name.'
                }), HTTP_404_NOT_FOUND
            
            total_pages = math.ceil(character_count/20)

            if (page>total_pages):
                return jsonify({
                    'success': False,
                    'error': 'Page number out of range.'
                }), HTTP_404_NOT_FOUND              
            
            characters = Characters.query.filter(Characters.name.ilike(f"%{name}%")).order_by(asc(Characters.id)).paginate(page=page, per_page=20)             

            characters_data = characters_schema.dump(characters)
            return jsonify({
                'success': True,
                'page': characters.page,
                'pages': characters.pages,
                'total': characters.total,
                'characters': characters_data
            }), HTTP_200_OK

    except Exception as e:
        raise