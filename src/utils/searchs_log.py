from src.database import SearchLogs, db
from flask import request

def log_search(search_result, search_result_cached = False):

    search_results_log_entry = SearchLogs(
        request_headers=dict(request.headers),
        ip_address=request.access_route[0],
        user_agent=request.headers.get('User-Agent'),
        endpoint=request.url,
        success = search_result.get('data').get('success'),
        status_code = search_result.get('http_code'),
        search_result_cached = search_result_cached
    )

    db.session.add(search_results_log_entry)
    db.session.commit()