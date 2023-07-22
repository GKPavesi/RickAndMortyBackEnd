from flask import Blueprint, jsonify, request
from src.database import Characters, character_schema, characters_schema
from sqlalchemy import asc
from src.constants.http_status_codes import *
from src.extensions.cache import cache
from src.utils.searchs_log import log_search
import math

search = Blueprint('search', __name__, url_prefix='/search')

@search.get('/')
@search.get('/<int:character_id>')
def handle_search(character_id=None):

    if (cache.get(request.url)):

        search_result = cache.get(request.url)

        log_search(search_result, search_result_cached = True)

        return jsonify(search_result.get('data')), search_result.get('http_code')

    try:
        if character_id is not None:
            character = Characters.query.get(character_id)
            if not character:
                search_result = {
                    'data': {
                        'success': False,
                        'error': 'Character not found'
                    },
                    'http_code': HTTP_404_NOT_FOUND
                }

                cache.set(request.url, search_result, timeout=600)
                log_search(search_result)

                return jsonify(search_result.get('data')), HTTP_404_NOT_FOUND

            character_data = character_schema.dump(character)
            
            search_result = {
                'data': {
                    'success': True,
                    'character': character_data                    
                },
                'http_code': HTTP_200_OK
            }

            cache.set(request.url, search_result, timeout=600)
            log_search(search_result)

            return jsonify(search_result.get('data')), HTTP_200_OK
        
        else:
            name = request.args.get('name')
            page = request.args.get('page', 1)

            try:
                page = int(page)
            except ValueError:
                search_result = {
                    'data': {
                        'success': False,
                        'error': 'Invalid page number. Please enter a valid integer.'
                    },
                    'http_code': HTTP_400_BAD_REQUEST
                }

                cache.set(request.url, search_result, timeout=600)
                log_search(search_result)

                return jsonify(search_result.get('data')), HTTP_400_BAD_REQUEST

            character_count = Characters.query.filter(Characters.name.ilike(f"%{name}%")).count()

            if not character_count:
                search_result = {
                    'data': {
                        'success': False,
                        'error': 'No characters found with the given name.'
                    },
                    'http_code': HTTP_404_NOT_FOUND
                }

                cache.set(request.url, search_result, timeout=600)
                log_search(search_result)

                return jsonify(search_result.get('data')), HTTP_404_NOT_FOUND
            
            total_pages = math.ceil(character_count/20)

            if (page>total_pages):

                search_result = {
                    'data': {
                        'success': False,
                        'error': 'Page number out of range.'
                    },
                    'http_code': HTTP_404_NOT_FOUND
                }

                cache.set(request.url, search_result, timeout=600)
                log_search(search_result)

                return jsonify(search_result.get('data')), HTTP_404_NOT_FOUND              
            
            characters = Characters.query.filter(Characters.name.ilike(f"%{name}%")).order_by(asc(Characters.id)).paginate(page=page, per_page=20)             

            characters_data = characters_schema.dump(characters)

            search_result = {
                'data': {
                    'success': True,
                    'page': characters.page,
                    'pages': characters.pages,
                    'total': characters.total,
                    'characters': characters_data
                },
                'http_code': HTTP_200_OK
            }

            cache.set(request.url, search_result, timeout=600)
            log_search(search_result)

            return jsonify(search_result.get('data')), HTTP_200_OK

    except Exception as e:
        raise