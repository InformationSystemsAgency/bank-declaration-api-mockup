"""
Data models for the Bank Data API
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import re


class SessionStatus(Enum):
    """Enumeration for session statuses"""
    PENDING = "PENDING"
    READY = "READY" 
    EXPIRED = "EXPIRED"
    DENIED = "DENIED"


@dataclass
class BankData:
    """Banking data of a citizen for tax declaration pre-filling"""
    DepositInterest: float
    DebtSecurityInterest: float
    SecuritiesDeductable: float
    NonPersonifiedIncome: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'DepositInterest': self.DepositInterest,
            'DebtSecurityInterest': self.DebtSecurityInterest,
            'SecuritiesDeductable': self.SecuritiesDeductable,
            'NonPersonifiedIncome': self.NonPersonifiedIncome
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BankData':
        """Create instance from dictionary"""
        return cls(
            DepositInterest=float(data.get('DepositInterest', 0)),
            DebtSecurityInterest=float(data.get('DebtSecurityInterest', 0)),
            SecuritiesDeductable=float(data.get('SecuritiesDeductable', 0)),
            NonPersonifiedIncome=float(data.get('NonPersonifiedIncome', 0))
        )


@dataclass  
class Session:
    """Represents a data request session"""
    session_id: str
    psn: str
    status: SessionStatus
    created_at: datetime
    expires_at: Optional[datetime]
    data: Optional[BankData] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            'sessionID': self.session_id,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'psn': self.psn
        }
        if self.expires_at:
            result['expiresAt'] = self.expires_at.isoformat()
        if self.data:
            result['data'] = self.data.to_dict()
        return result


class ValidationError(Exception):
    """Exception raised for validation errors"""
    pass


def validate_psn(psn: str) -> bool:
    """Validate PSN format - must be exactly 10 digits"""
    pattern = r'^[0-9]{10}$'
    return bool(re.match(pattern, psn))


def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format"""
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    return bool(re.match(pattern, uuid_str))


def generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid.uuid4())