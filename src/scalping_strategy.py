"""
Scalping strategy module.
Implements basic scalping trading logic.
"""
import logging
from typing import Optional, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScalpingStrategy:
    """
    Scalping trading strategy.
    
    Scalping is a trading strategy that attempts to profit from small price changes,
    with traders entering and exiting positions quickly.
    """
    
    def __init__(self, profit_target: float, stop_loss: float, position_size: int):
        """
        Initialize scalping strategy.
        
        Args:
            profit_target: Target profit in price units
            stop_loss: Stop loss in price units
            position_size: Size of each position
        """
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.position_size = position_size
        self.current_position: Optional[Dict] = None
        self.entry_price: Optional[float] = None
        self.position_side: Optional[str] = None  # 'LONG' or 'SHORT'
        
    def should_enter_long(self, current_price: float, bid: float, ask: float) -> bool:
        """
        Determine if we should enter a long position.
        
        Basic scalping logic: Enter when bid-ask spread is favorable.
        
        Args:
            current_price: Current market price
            bid: Current bid price
            ask: Current ask price
            
        Returns:
            True if should enter long position
        """
        # Only enter if no current position
        if self.current_position is not None:
            return False
        
        # Simple logic: Enter long if spread is tight (indicates liquidity)
        spread = ask - bid
        if spread > 0 and spread < current_price * 0.0001:  # Spread less than 0.01%
            return True
        
        return False
    
    def should_enter_short(self, current_price: float, bid: float, ask: float) -> bool:
        """
        Determine if we should enter a short position.
        
        Args:
            current_price: Current market price
            bid: Current bid price
            ask: Current ask price
            
        Returns:
            True if should enter short position
        """
        # Only enter if no current position
        if self.current_position is not None:
            return False
        
        # Similar logic to long, can be enhanced with indicators
        spread = ask - bid
        if spread > 0 and spread < current_price * 0.0001:
            return True
        
        return False
    
    def should_exit_position(self, current_price: float) -> tuple[bool, str]:
        """
        Determine if we should exit current position.
        
        Args:
            current_price: Current market price
            
        Returns:
            Tuple of (should_exit, reason)
        """
        if self.current_position is None or self.entry_price is None:
            return False, ""
        
        # Use small epsilon for floating point comparison
        epsilon = 1e-10
        
        if self.position_side == 'LONG':
            profit = current_price - self.entry_price
            
            # Check profit target
            if profit >= self.profit_target - epsilon:
                return True, "PROFIT_TARGET"
            
            # Check stop loss
            if profit <= -self.stop_loss + epsilon:
                return True, "STOP_LOSS"
                
        elif self.position_side == 'SHORT':
            profit = self.entry_price - current_price
            
            # Check profit target
            if profit >= self.profit_target - epsilon:
                return True, "PROFIT_TARGET"
            
            # Check stop loss
            if profit <= -self.stop_loss + epsilon:
                return True, "STOP_LOSS"
        
        return False, ""
    
    def enter_position(self, side: str, price: float):
        """
        Record position entry.
        
        Args:
            side: 'LONG' or 'SHORT'
            price: Entry price
        """
        self.current_position = {
            'side': side,
            'entry_price': price,
            'entry_time': datetime.now(),
            'size': self.position_size
        }
        self.entry_price = price
        self.position_side = side
        logger.info(f"Entered {side} position at {price}")
    
    def exit_position(self, price: float, reason: str):
        """
        Record position exit.
        
        Args:
            price: Exit price
            reason: Reason for exit
        """
        if self.current_position:
            profit = 0
            if self.position_side == 'LONG':
                profit = (price - self.entry_price) * self.position_size
            elif self.position_side == 'SHORT':
                profit = (self.entry_price - price) * self.position_size
            
            logger.info(f"Exited {self.position_side} position at {price}. "
                       f"Reason: {reason}. Profit: {profit:.2f}")
            
            self.current_position = None
            self.entry_price = None
            self.position_side = None
    
    def get_position_info(self) -> Optional[Dict]:
        """Get current position information."""
        return self.current_position
