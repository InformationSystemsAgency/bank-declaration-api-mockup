"""
Core API routes for the Bank Data API
Implements the main data exchange endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import validate_psn, validate_uuid, ValidationError, SessionStatus
from app.services.session_manager import session_manager
from app.services.mock_data_service import mock_bank_service
import threading
import time

# Import logger after other imports to avoid circular import issues
try:
    from app.config import get_logger
    logger = get_logger('routes.core')
except Exception as e:
    # Fallback logging if config import fails
    import logging
    logger = logging.getLogger('app.routes.core')
    print(f"Warning: Could not get configured logger for core routes: {e}")

print(f"Core routes logger level: {logger.level}")
core_bp = Blueprint('core', __name__)


def log_request(request_id: str, operation: str, details: str):
    """Log request with request ID if provided"""
    if request_id:
        logger.info(f"[{request_id}] {operation}: {details}")
    else:
        logger.info(f"{operation}: {details}")


def simulate_consent_process(session_id: str, psn: str):
    """
    Simulate the consent acquisition process in a separate thread.
    In a real implementation, this would integrate with the bank's consent management system.
    """
    def consent_worker():
        time.sleep(2)  # Simulate time for consent process
        
        # Check if citizen will deny consent
        if mock_bank_service.will_deny_consent(psn):
            session_manager.update_session_status(session_id, SessionStatus.DENIED)
            logger.info(f"Consent denied for session {session_id}")
            return
        
        # Simulate longer processing for some PSNs
        if mock_bank_service.requires_slow_processing(psn):
            time.sleep(5)
        
        # Get the banking data
        bank_data = mock_bank_service.get_banking_data(psn)
        if bank_data:
            session_manager.update_session_status(session_id, SessionStatus.READY, bank_data)
            logger.info(f"Data ready for session {session_id}")
        else:
            session_manager.update_session_status(session_id, SessionStatus.EXPIRED)
            logger.info(f"No data available, expired session {session_id}")
    
    # Start consent process in background
    consent_thread = threading.Thread(target=consent_worker)
    consent_thread.daemon = True
    consent_thread.start()


@core_bp.route('/citizen/<psn>/BankingData', methods=['GET'])
def data_request(psn: str):
    """
    Initiates the data transfer process.
    Returns a session ID if data might be available based on consent.
    """
    request_id = request.headers.get('X-Request-ID')
    log_request(request_id, "data_request", f"Received request for PSN {psn}")
    
    # Validate PSN format
    if not validate_psn(psn):
        log_request(request_id, "data_request", f"Invalid PSN format: {psn}")
        return jsonify({"error": "Invalid PSN format"}), 400
    
    # Check if bank has data for this PSN
    if not mock_bank_service.has_data_for_psn(psn):
        log_request(request_id, "data_request", f"No data available for PSN {psn}")
        return jsonify({"error": "No data available for this citizen"}), 404
    
    # Create new session (this will expire any existing session for the PSN)
    session = session_manager.create_session(psn)
    
    # Start the consent acquisition process
    simulate_consent_process(session.session_id, psn)
    
    log_request(request_id, "data_request", f"Created session {session.session_id} for PSN {psn}")
    
    # Return session info
    response = {
        "sessionID": session.session_id,
        "expiresAt": session.expires_at.isoformat() if session.expires_at else None
    }
    
    return jsonify(response), 200


@core_bp.route('/citizen/<psn>/BankingData/<session_id>', methods=['GET'])
def get_data(psn: str, session_id: str):
    """
    Allows downloading citizen data that was previously requested.
    Requires both PSN and session ID to match.
    """

    request_id = request.headers.get('X-Request-ID')
    log_request(request_id, "get_data", f"Data retrieval request for PSN {psn}, session {session_id}")
    
    # Validate inputs
    if not validate_psn(psn):
        log_request(request_id, "get_data", f"Invalid PSN format: {psn}")
        return jsonify({"error": "Invalid PSN format"}), 400
    
    if not validate_uuid(session_id):
        log_request(request_id, "get_data", f"Invalid session ID format: {session_id}")
        return jsonify({"error": "Invalid session ID format"}), 400
    
    log_request(request_id, "get_data", f"Perfectly valid sessionID: {session_id}")
    
    # Get session that matches both PSN and session ID
    session = session_manager.get_session_for_psn_and_id(psn, session_id)
    
    if not session:
        log_request(request_id, "get_data", f"No matching session found for PSN {psn} and session {session_id}")
        return jsonify({"error": "No matching session found"}), 404
    
    # Check session status
    if session.status != SessionStatus.READY:
        log_request(request_id, "get_data", f"Session {session_id} not ready (status: {session.status.value})")
        return jsonify({"error": f"Session not ready (status: {session.status.value})"}), 404
    
    # Return the banking data
    if session.data:
        log_request(request_id, "get_data", f"Returning banking data for PSN {psn}")
        return jsonify(session.data.to_dict()), 200
    else:
        log_request(request_id, "get_data", f"No data available for session {session_id}")
        return jsonify({"error": "No data available"}), 404