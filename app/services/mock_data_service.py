"""
Mock data service for simulating bank data
In a real implementation, this would connect to actual bank systems
"""

from typing import Optional
from app.models import BankData
import random

# Import logger after other imports to avoid circular import issues
try:
    from app.config import get_logger
    logger = get_logger('services.mock_data')
    logger.debug("Mock data service logger initialized")
except Exception as e:
    # Fallback logging if config import fails
    import logging
    logger = logging.getLogger('app.services.mock_data')
    print(f"Warning: Could not get configured logger: {e}")


class MockBankDataService:
    """Mock service that simulates bank data retrieval"""
    
    def __init__(self):
        """Initialize with some mock data for known PSNs"""
        # Mock database of citizens with banking data
        self._mock_data = {
            "1234567890": BankData(
                DepositInterest=250000,
                DebtSecurityInterest=0,
                SecuritiesDeductable=45000,
                NonPersonifiedIncome=5640
            ),
            "9876543210": BankData(
                DepositInterest=180000,
                DebtSecurityInterest=25000,
                SecuritiesDeductable=15000,
                NonPersonifiedIncome=3200
            ),
            "5555555555": BankData(
                DepositInterest=0,
                DebtSecurityInterest=0,
                SecuritiesDeductable=0,
                NonPersonifiedIncome=0
            )
        }
        
        # PSNs that exist but will deny consent
        self._denied_psns = {"1111111111", "2222222222"}
        
        # PSNs that will simulate long processing (stay PENDING longer)
        self._slow_processing_psns = {"3333333333"}
    
    def has_data_for_psn(self, psn: str) -> bool:
        """Check if the bank has data for this PSN"""
        return psn in self._mock_data or psn in self._denied_psns or psn in self._slow_processing_psns
    
    def will_deny_consent(self, psn: str) -> bool:
        """Check if this PSN will deny consent"""
        return psn in self._denied_psns
    
    def requires_slow_processing(self, psn: str) -> bool:
        """Check if this PSN requires slower processing (for demo purposes)"""
        return psn in self._slow_processing_psns
    
    def get_banking_data(self, psn: str) -> Optional[BankData]:
        """
        Retrieve banking data for a PSN.
        Returns None if no data available or consent not given.
        """
        if psn in self._mock_data:
            logger.info(f"Retrieved banking data for PSN {psn}")
            return self._mock_data[psn]
        
        # For demo purposes, generate random data for unknown but valid PSNs
        if psn not in self._denied_psns:
            logger.info(f"Generating mock data for PSN {psn}")
            return BankData(
                DepositInterest=random.randint(0, 500000),
                DebtSecurityInterest=random.randint(0, 100000),
                SecuritiesDeductable=random.randint(0, 100000),
                NonPersonifiedIncome=random.randint(0, 50000)
            )
        
        logger.info(f"No data available for PSN {psn}")
        return None


# Global instance
mock_bank_service = MockBankDataService()