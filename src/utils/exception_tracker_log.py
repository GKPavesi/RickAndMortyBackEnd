from src.database import db, ExceptionTracker
from flask import request
import traceback

def log_exception(e):
    error_message = str(e)
    traceback_str = traceback.format_exc()

    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    endpoint = request.url
    http_method = request.method

    error_log_entry = ExceptionTracker(
        error_message=error_message,
        request_headers=dict(request.headers),
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint,
        http_method=http_method,
        traceback=traceback_str,
    )
    db.session.add(error_log_entry)
    db.session.commit()    