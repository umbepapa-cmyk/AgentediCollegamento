"""
Main trading agent application.
Coordinates IB Gateway connection and scalping strategy execution.
"""
import logging
import time
import signal
import sys
from typing import Optional

from src.config import config
from src.ib_connection import IBConnection
from src.scalping_strategy import ScalpingStrategy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingAgent:
    """Main trading agent that connects to IB Gateway and executes scalping strategy."""
    
    def __init__(self):
        """Initialize the trading agent."""
        self.running = False
        self.ib_connection: Optional[IBConnection] = None
        self.strategy: Optional[ScalpingStrategy] = None
        self.contract = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown signals."""
        logger.info("Shutdown signal received. Stopping agent...")
        self.stop()
        sys.exit(0)
    
    def initialize(self) -> bool:
        """
        Initialize connection and strategy.
        
        Returns:
            True if initialization successful
        """
        try:
            # Validate configuration
            config.validate()
            logger.info("Configuration validated successfully")
            
            # Initialize IB connection
            self.ib_connection = IBConnection(
                host=config.IB_HOST,
                port=config.IB_PORT,
                client_id=config.IB_CLIENT_ID
            )
            
            # Connect to IB Gateway
            if not self.ib_connection.connect():
                logger.error("Failed to connect to IB Gateway")
                return False
            
            # Create contract
            self.contract = self.ib_connection.create_forex_contract(
                symbol=config.SYMBOL,
                exchange=config.EXCHANGE
            )
            logger.info(f"Created contract for {config.SYMBOL}")
            
            # Initialize strategy
            self.strategy = ScalpingStrategy(
                profit_target=config.PROFIT_TARGET,
                stop_loss=config.STOP_LOSS,
                position_size=config.POSITION_SIZE
            )
            logger.info("Scalping strategy initialized")
            
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False
    
    def run(self):
        """Main trading loop."""
        if not self.initialize():
            logger.error("Agent initialization failed. Exiting.")
            return
        
        logger.info("Trading agent started. Press Ctrl+C to stop.")
        self.running = True
        
        try:
            while self.running:
                self._execute_trading_cycle()
                time.sleep(1)  # Wait 1 second between cycles
                
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
        finally:
            self.stop()
    
    def _execute_trading_cycle(self):
        """Execute one cycle of the trading strategy."""
        try:
            # Check connection
            if not self.ib_connection.is_connected():
                logger.warning("Lost connection to IB Gateway. Attempting to reconnect...")
                if not self.ib_connection.connect():
                    logger.error("Reconnection failed")
                    self.running = False
                    return
            
            # Get market data
            ticker = self.ib_connection.ib.reqMktData(self.contract, '', False, False)
            self.ib_connection.ib.sleep(0.5)
            
            current_price = ticker.marketPrice() if ticker.marketPrice() > 0 else ticker.last
            bid = ticker.bid if ticker.bid > 0 else current_price
            ask = ticker.ask if ticker.ask > 0 else current_price
            
            if not current_price or current_price <= 0:
                logger.debug("No valid market price available")
                return
            
            # Check if we should exit current position
            if self.strategy.current_position:
                should_exit, reason = self.strategy.should_exit_position(current_price)
                if should_exit:
                    self._exit_position(current_price, reason)
            
            # Check if we should enter new position
            else:
                if self.strategy.should_enter_long(current_price, bid, ask):
                    self._enter_position('LONG', current_price)
                elif self.strategy.should_enter_short(current_price, bid, ask):
                    self._enter_position('SHORT', current_price)
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
    
    def _enter_position(self, side: str, price: float):
        """
        Enter a new position.
        
        Args:
            side: 'LONG' or 'SHORT'
            price: Entry price
        """
        action = 'BUY' if side == 'LONG' else 'SELL'
        
        # Place order
        trade = self.ib_connection.place_order(
            contract=self.contract,
            action=action,
            quantity=self.strategy.position_size
        )
        
        if trade:
            # Record in strategy
            self.strategy.enter_position(side, price)
            logger.info(f"Entered {side} position: {action} {self.strategy.position_size} @ {price}")
    
    def _exit_position(self, price: float, reason: str):
        """
        Exit current position.
        
        Args:
            price: Exit price
            reason: Reason for exit
        """
        if not self.strategy.current_position:
            return
        
        # Reverse action
        action = 'SELL' if self.strategy.position_side == 'LONG' else 'BUY'
        
        # Place closing order
        trade = self.ib_connection.place_order(
            contract=self.contract,
            action=action,
            quantity=self.strategy.position_size
        )
        
        if trade:
            # Record in strategy
            self.strategy.exit_position(price, reason)
            logger.info(f"Exited position: {action} {self.strategy.position_size} @ {price} ({reason})")
    
    def stop(self):
        """Stop the trading agent."""
        logger.info("Stopping trading agent...")
        self.running = False
        
        # Close any open positions before disconnecting
        if self.strategy and self.strategy.current_position:
            logger.info("Closing open position...")
            current_price = self.ib_connection.get_market_price(self.contract)
            if current_price:
                self._exit_position(current_price, "AGENT_SHUTDOWN")
        
        # Disconnect from IB
        if self.ib_connection:
            self.ib_connection.disconnect()
        
        logger.info("Trading agent stopped")


def main():
    """Main entry point."""
    logger.info("Starting IB Gateway Scalping Agent...")
    agent = TradingAgent()
    agent.run()


if __name__ == '__main__':
    main()
