from src.database import db, ExceptionTracker
from flask import request
import traceback

def log_exception(e):
    
    error_log_entry = ExceptionTracker(
        error_message=str(e),
        request_headers=dict(request.headers),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        endpoint=request.url,
        http_method=request.method,
        traceback=traceback.format_exc(),
    )
    db.session.add(error_log_entry)
    db.session.commit()    