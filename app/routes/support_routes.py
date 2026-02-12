"""
Support API routes for the Bank Data API
Implements session status checking and other supporting endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import validate_uuid, SessionStatus
from app.services.session_manager import session_manager
from app.config import get_logger
from datetime import datetime

logger = get_logger('routes.support')

support_bp = Blueprint('support', __name__)


def log_request(request_id: str, operation: str, details: str):
    """Log request with request ID if provided"""
    if request_id:
        logger.info(f"[{request_id}] {operation}: {details}")
    else:
        logger.info(f"{operation}: {details}")


# Rate limiting - simple in-memory store (in production, use Redis or similar)
from app.config import Config
config = Config()

_rate_limit_store = {}
_rate_limit_window = config.RATE_LIMIT_WINDOW_SECONDS
_max_requests_per_minute = config.RATE_LIMIT_MAX_REQUESTS

logger.info(f"Rate limiting configured: {_max_requests_per_minute} requests per {_rate_limit_window} seconds")


def check_rate_limit(session_id: str) -> bool:
    """Simple rate limiting check"""
    current_time = datetime.now().timestamp()
    
    if session_id not in _rate_limit_store:
        _rate_limit_store[session_id] = []
    
    # Clean old requests outside the window
    requests = _rate_limit_store[session_id]
    _rate_limit_store[session_id] = [req_time for req_time in requests 
                                   if current_time - req_time < _rate_limit_window]
    
    # Check if we're over the limit
    if len(_rate_limit_store[session_id]) >= _max_requests_per_minute:
        return False
    
    # Add this request
    _rate_limit_store[session_id].append(current_time)
    return True


@support_bp.route('/request/<session_id>', methods=['GET'])
def get_session_status(session_id: str):
    """
    Allows the requesting party to poll for the status of the data request.
    Returns different HTTP status codes based on session status.
    """
    request_id = request.headers.get('X-Request-ID')
    log_request(request_id, "get_session_status", f"Status check for session {session_id}")
    
    # Validate session ID format
    if not validate_uuid(session_id):
        log_request(request_id, "get_session_status", f"Invalid session ID format: {session_id}")
        return jsonify({"error": "Invalid session ID format"}), 400
    
    # Check rate limiting
    if not check_rate_limit(session_id):
        log_request(request_id, "get_session_status", f"Rate limit exceeded for session {session_id}")
        return jsonify({"error": "Too many requests"}), 429
    
    # Get session
    session = session_manager.get_session(session_id)
    
    if not session:
        log_request(request_id, "get_session_status", f"Session {session_id} not found or expired")
        return jsonify({"error": "Session not found or expired"}), 404
    
    # Return appropriate status code based on session status
    if session.status == SessionStatus.READY:
        log_request(request_id, "get_session_status", f"Session {session_id} is ready")
        return '', 200
    elif session.status == SessionStatus.PENDING:
        log_request(request_id, "get_session_status", f"Session {session_id} is pending")
        return '', 202
    elif session.status == SessionStatus.DENIED:
        log_request(request_id, "get_session_status", f"Session {session_id} was denied")
        return '', 590
    else:  # EXPIRED or unknown status
        log_request(request_id, "get_session_status", f"Session {session_id} has expired")
        return '', 404