"""
Session management service for the Bank Data API
"""

from typing import Optional, Dict
from datetime import datetime, timedelta
from app.models import Session, SessionStatus, BankData, generate_uuid
from app.config import get_logger
import threading

logger = get_logger('services.session_manager')


class SessionManager:
    """Manages data request sessions"""
    
    def __init__(self, default_ttl_minutes: Optional[int] = None):
        """Initialize the session manager"""
        from app.config import Config
        config = Config()
        
        self._sessions: Dict[str, Session] = {}
        self._psn_sessions: Dict[str, str] = {}  # PSN -> session_id mapping
        self._lock = threading.Lock()
        self._default_ttl_minutes = default_ttl_minutes or config.SESSION_TTL_MINUTES
        
        logger.info(f"SessionManager initialized with TTL: {self._default_ttl_minutes} minutes")
        
    def create_session(self, psn: str) -> Session:
        """
        Create a new session for a PSN.
        Only one valid session per PSN is allowed.
        """
        with self._lock:
            # Expire any existing session for this PSN
            if psn in self._psn_sessions:
                old_session_id = self._psn_sessions[psn]
                if old_session_id in self._sessions:
                    self._sessions[old_session_id].status = SessionStatus.EXPIRED
                    logger.info(f"Expired previous session {old_session_id} for PSN {psn}")
            
            # Create new session. Normalize to upper case for consistency
            session_id = generate_uuid().upper()
            expires_at = datetime.now() + timedelta(minutes=self._default_ttl_minutes)

            session = Session(
                session_id=session_id,
                psn=psn,
                status=SessionStatus.PENDING,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            self._sessions[session_id] = session
            self._psn_sessions[psn] = session_id
            
            logger.info(f"Created new session {session_id} for PSN {psn}")
            return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID"""
        logger.debug(f"Retrieving session {session_id}")
        with self._lock:
            logger.debug(f"Current sessions: {list(self._sessions.keys())}")
            session = self._sessions.get(session_id.upper())
            logger.debug(f"Retrieved session: {session}")
            if session:
                # Check if session has expired
                if session.expires_at and datetime.now() > session.expires_at:
                    session.status = SessionStatus.EXPIRED
                    logger.info(f"Session {session_id} has expired")
            return session
    
    def update_session_status(self, session_id: str, status: SessionStatus, data: Optional[BankData] = None) -> bool:
        """Update session status and optionally set data"""
        with self._lock:
            if session_id in self._sessions:
                session = self._sessions[session_id.upper()]
                session.status = status
                if data:
                    session.data = data
                logger.info(f"Updated session {session_id} status to {status.value}")
                return True
            return False
    
    def get_session_for_psn_and_id(self, psn: str, session_id: str) -> Optional[Session]:
        """Get session that matches both PSN and session ID"""
        session = self.get_session(session_id)
        if session and session.psn == psn:
            return session
        return None
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from memory"""
        with self._lock:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session in self._sessions.items():
                if (session.expires_at and current_time > session.expires_at) or \
                   session.status == SessionStatus.EXPIRED:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                session = self._sessions.pop(session_id, None)
                if session and session.psn in self._psn_sessions:
                    if self._psn_sessions[session.psn] == session_id:
                        del self._psn_sessions[session.psn]
                logger.info(f"Cleaned up expired session {session_id}")


# Global session manager instance
session_manager = SessionManager()