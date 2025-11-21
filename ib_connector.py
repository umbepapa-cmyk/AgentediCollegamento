"""
Modulo per la connessione a IB Gateway
"""

from ib_insync import IB, Contract, MarketOrder, LimitOrder, util
import logging
import asyncio

logger = logging.getLogger(__name__)


class IBConnector:
    """Gestisce la connessione con IB Gateway"""
    
    def __init__(self, host='127.0.0.1', port=4002, client_id=1):
        """
        Inizializza il connector IB
        
        Args:
            host: Host IB Gateway
            port: Porta IB Gateway
            client_id: Client ID univoco
        """
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False
        
    def connect(self):
        """Connette a IB Gateway"""
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self.connected = True
            logger.info(f"Connesso a IB Gateway su {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Errore connessione IB Gateway: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnette da IB Gateway"""
        if self.connected:
            self.ib.disconnect()
            self.connected = False
            logger.info("Disconnesso da IB Gateway")
    
    def create_forex_contract(self, symbol, exchange='IDEALPRO'):
        """
        Crea un contratto forex
        
        Args:
            symbol: Simbolo coppia (es. 'EUR.USD')
            exchange: Exchange (default IDEALPRO per forex)
            
        Returns:
            Contract object
        """
        base, quote = symbol.split('.')
        contract = Contract()
        contract.symbol = base
        contract.secType = 'CASH'
        contract.currency = quote
        contract.exchange = exchange
        return contract
    
    def get_market_price(self, contract):
        """
        Ottiene il prezzo di mercato corrente
        
        Args:
            contract: Contract object
            
        Returns:
            Tuple (bid, ask, last)
        """
        try:
            ticker = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(1)  # Attendi aggiornamento dati
            
            bid = ticker.bid if ticker.bid and ticker.bid > 0 else None
            ask = ticker.ask if ticker.ask and ticker.ask > 0 else None
            last = ticker.last if ticker.last and ticker.last > 0 else None
            
            self.ib.cancelMktData(contract)
            return bid, ask, last
        except Exception as e:
            logger.error(f"Errore nel recupero prezzo: {e}")
            return None, None, None
    
    def place_market_order(self, contract, action, quantity):
        """
        Piazza un ordine market
        
        Args:
            contract: Contract object
            action: 'BUY' o 'SELL'
            quantity: Quantità
            
        Returns:
            Trade object
        """
        try:
            order = MarketOrder(action, quantity)
            trade = self.ib.placeOrder(contract, order)
            logger.info(f"Ordine market piazzato: {action} {quantity} {contract.symbol}")
            return trade
        except Exception as e:
            logger.error(f"Errore piazzamento ordine market: {e}")
            return None
    
    def place_limit_order(self, contract, action, quantity, limit_price):
        """
        Piazza un ordine limit
        
        Args:
            contract: Contract object
            action: 'BUY' o 'SELL'
            quantity: Quantità
            limit_price: Prezzo limite
            
        Returns:
            Trade object
        """
        try:
            order = LimitOrder(action, quantity, limit_price)
            trade = self.ib.placeOrder(contract, order)
            logger.info(f"Ordine limit piazzato: {action} {quantity} {contract.symbol} @ {limit_price}")
            return trade
        except Exception as e:
            logger.error(f"Errore piazzamento ordine limit: {e}")
            return None
    
    def get_positions(self):
        """
        Ottiene le posizioni aperte
        
        Returns:
            Lista di posizioni
        """
        try:
            positions = self.ib.positions()
            return positions
        except Exception as e:
            logger.error(f"Errore recupero posizioni: {e}")
            return []
    
    def get_account_summary(self):
        """
        Ottiene il summary dell'account
        
        Returns:
            Lista di account values
        """
        try:
            account_values = self.ib.accountSummary()
            return account_values
        except Exception as e:
            logger.error(f"Errore recupero account summary: {e}")
            return []
    
    def cancel_order(self, trade):
        """
        Cancella un ordine
        
        Args:
            trade: Trade object da cancellare
        """
        try:
            self.ib.cancelOrder(trade.order)
            logger.info(f"Ordine cancellato: {trade.order.orderId}")
        except Exception as e:
            logger.error(f"Errore cancellazione ordine: {e}")
