"""
Configuration module for IB Gateway connection and trading parameters.
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for IB Gateway and scalping strategy."""
    
    # IB Gateway connection settings
    IB_HOST: str = os.getenv('IB_HOST', '127.0.0.1')
    IB_PORT: int = int(os.getenv('IB_PORT', '4002'))
    IB_CLIENT_ID: int = int(os.getenv('IB_CLIENT_ID', '1'))
    
    # Trading instrument settings
    SYMBOL: str = os.getenv('SYMBOL', 'EUR.USD')
    EXCHANGE: str = os.getenv('EXCHANGE', 'IDEALPRO')
    
    # Scalping strategy parameters
    TICK_SIZE: float = float(os.getenv('TICK_SIZE', '0.00005'))
    PROFIT_TARGET: float = float(os.getenv('PROFIT_TARGET', '0.0002'))
    STOP_LOSS: float = float(os.getenv('STOP_LOSS', '0.0001'))
    POSITION_SIZE: int = int(os.getenv('POSITION_SIZE', '20000'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration parameters."""
        if cls.PROFIT_TARGET <= 0:
            raise ValueError("PROFIT_TARGET must be positive")
        if cls.STOP_LOSS <= 0:
            raise ValueError("STOP_LOSS must be positive")
        if cls.POSITION_SIZE <= 0:
            raise ValueError("POSITION_SIZE must be positive")
        return True


config = Config()
