"""
IB Gateway connection module.
Handles connection to Interactive Brokers Gateway for trading operations.
"""
import logging
from ib_insync import IB, Contract, Order, MarketOrder, LimitOrder, util
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IBConnection:
    """Manages connection to IB Gateway."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 4002, client_id: int = 1):
        """
        Initialize IB connection.
        
        Args:
            host: IB Gateway host address
            port: IB Gateway port (4002 for paper trading, 4001 for live)
            client_id: Unique client identifier
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()
        self._connected = False
        
    def connect(self) -> bool:
        """
        Establish connection to IB Gateway.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self._connected = True
            logger.info(f"Connected to IB Gateway at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            self._connected = False
            return False
    
    def disconnect(self):
        """Disconnect from IB Gateway."""
        if self._connected:
            self.ib.disconnect()
            self._connected = False
            logger.info("Disconnected from IB Gateway")
    
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._connected and self.ib.isConnected()
    
    def create_forex_contract(self, symbol: str, exchange: str = 'IDEALPRO') -> Contract:
        """
        Create a forex contract.
        
        Args:
            symbol: Currency pair (e.g., 'EUR.USD')
            exchange: Exchange name (default: IDEALPRO for forex)
            
        Returns:
            Contract object
        """
        base, quote = symbol.split('.')
        contract = Contract()
        contract.symbol = base
        contract.secType = 'CASH'
        contract.exchange = exchange
        contract.currency = quote
        return contract
    
    def get_market_price(self, contract: Contract) -> Optional[float]:
        """
        Get current market price for a contract.
        
        Args:
            contract: IB Contract object
            
        Returns:
            Current market price or None if unavailable
        """
        try:
            ticker = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(1)  # Wait for data
            
            if ticker.marketPrice() and ticker.marketPrice() > 0:
                return ticker.marketPrice()
            elif ticker.last and ticker.last > 0:
                return ticker.last
            elif ticker.bid and ticker.ask:
                return (ticker.bid + ticker.ask) / 2
            
            return None
        except Exception as e:
            logger.error(f"Error getting market price: {e}")
            return None
    
    def place_order(self, contract: Contract, action: str, quantity: int, 
                   limit_price: Optional[float] = None) -> Optional[object]:
        """
        Place an order.
        
        Args:
            contract: IB Contract object
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            limit_price: Limit price for limit orders (None for market orders)
            
        Returns:
            Trade object or None if failed
        """
        try:
            if limit_price:
                order = LimitOrder(action, quantity, limit_price)
            else:
                order = MarketOrder(action, quantity)
            
            trade = self.ib.placeOrder(contract, order)
            logger.info(f"Placed {action} order for {quantity} units")
            return trade
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def get_positions(self):
        """Get current positions."""
        return self.ib.positions()
    
    def get_account_values(self):
        """Get account values."""
        return self.ib.accountValues()
