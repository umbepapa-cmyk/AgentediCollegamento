"""
Agente di Scalping per IB Gateway
Main module per l'esecuzione del trading bot
"""

import logging
import time
from datetime import datetime, timedelta
from ib_connector import IBConnector
from scalping_strategy import ScalpingStrategy
import config

# Costanti
SECONDS_PER_MINUTE = 60  # Conversione secondi a minuti

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scalping_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ScalpingAgent:
    """Agente principale per trading scalping su IB Gateway"""
    
    def __init__(self):
        """Inizializza l'agente di scalping"""
        self.connector = IBConnector(
            host=config.IB_HOST,
            port=config.IB_PORT,
            client_id=config.IB_CLIENT_ID
        )
        self.strategy = ScalpingStrategy(
            ema_fast=config.EMA_FAST,
            ema_slow=config.EMA_SLOW,
            rsi_period=config.RSI_PERIOD
        )
        self.contract = None
        self.active_positions = {}  # {position_id: {entry_price, action, stop_loss, take_profit, quantity}}
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.start_of_day = datetime.now().date()
        self.running = False
        
    def connect(self):
        """Connette a IB Gateway"""
        success = self.connector.connect()
        if success:
            self.contract = self.connector.create_forex_contract(
                config.SYMBOL,
                config.EXCHANGE
            )
            logger.info(f"Contratto creato per {config.SYMBOL}")
        return success
    
    def disconnect(self):
        """Disconnette da IB Gateway"""
        self.connector.disconnect()
        self.running = False
    
    def check_risk_limits(self):
        """
        Verifica i limiti di rischio
        
        Returns:
            True se i limiti sono rispettati
        """
        # Reset giornaliero
        if datetime.now().date() != self.start_of_day:
            logger.info("Nuovo giorno - reset contatori")
            self.daily_pnl = 0.0
            self.daily_trades = 0
            self.start_of_day = datetime.now().date()
        
        # Verifica perdita massima giornaliera
        if self.daily_pnl <= config.MAX_DAILY_LOSS:
            logger.warning(f"STOP: Perdita massima giornaliera raggiunta ({self.daily_pnl:.2f} USD)")
            return False
        
        # Verifica numero massimo di trade
        if self.daily_trades >= config.MAX_DAILY_TRADES:
            logger.warning(f"STOP: Numero massimo di trade giornalieri raggiunto ({self.daily_trades})")
            return False
        
        # Verifica numero massimo posizioni aperte
        if len(self.active_positions) >= config.MAX_POSITIONS:
            logger.debug(f"Numero massimo posizioni aperte raggiunto ({len(self.active_positions)})")
            return False
        
        return True
    
    def open_position(self, action):
        """
        Apre una nuova posizione
        
        Args:
            action: 'BUY' o 'SELL'
        """
        if not self.check_risk_limits():
            return
        
        # Ottieni prezzo corrente
        bid, ask, last = self.connector.get_market_price(self.contract)
        
        if action == 'BUY':
            entry_price = ask if ask else last
        else:  # SELL
            entry_price = bid if bid else last
        
        if not entry_price:
            logger.error("Impossibile ottenere prezzo di entrata")
            return
        
        # Calcola stop loss e take profit
        stop_loss = self.strategy.calculate_stop_loss(
            entry_price, action, config.STOP_LOSS
        )
        take_profit = self.strategy.calculate_take_profit(
            entry_price, action, config.PROFIT_TARGET
        )
        
        # Piazza ordine
        trade = self.connector.place_market_order(
            self.contract, action, config.POSITION_SIZE
        )
        
        if trade:
            position_id = f"{action}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.active_positions[position_id] = {
                'entry_price': entry_price,
                'action': action,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'quantity': config.POSITION_SIZE,
                'trade': trade
            }
            self.daily_trades += 1
            logger.info(f"Posizione aperta: {position_id}")
            logger.info(f"Entry: {entry_price:.5f}, SL: {stop_loss:.5f}, TP: {take_profit:.5f}")
    
    def close_position(self, position_id):
        """
        Chiude una posizione esistente
        
        Args:
            position_id: ID della posizione da chiudere
        """
        if position_id not in self.active_positions:
            return
        
        position = self.active_positions[position_id]
        
        # Inverti l'azione per chiudere
        close_action = 'SELL' if position['action'] == 'BUY' else 'BUY'
        
        # Piazza ordine di chiusura
        trade = self.connector.place_market_order(
            self.contract, close_action, position['quantity']
        )
        
        if trade:
            # Ottieni prezzo di uscita
            bid, ask, last = self.connector.get_market_price(self.contract)
            exit_price = bid if close_action == 'SELL' else ask
            if not exit_price:
                exit_price = last
            
            # Calcola P&L
            if position['action'] == 'BUY':
                pnl = (exit_price - position['entry_price']) * position['quantity']
            else:
                pnl = (position['entry_price'] - exit_price) * position['quantity']
            
            self.daily_pnl += pnl
            
            logger.info(f"Posizione chiusa: {position_id}")
            logger.info(f"Exit: {exit_price:.5f}, P&L: {pnl:.2f} USD, P&L giornaliero: {self.daily_pnl:.2f} USD")
            
            # Rimuovi posizione
            del self.active_positions[position_id]
    
    def manage_positions(self):
        """Gestisce le posizioni aperte (stop loss e take profit)"""
        if not self.active_positions:
            return
        
        # Ottieni prezzo corrente
        bid, ask, last = self.connector.get_market_price(self.contract)
        current_price = last if last else (bid + ask) / 2 if bid and ask else None
        
        if not current_price:
            logger.error("Impossibile ottenere prezzo corrente per gestione posizioni")
            return
        
        # Aggiungi prezzo alla strategia
        self.strategy.add_price(current_price)
        
        # Verifica ogni posizione
        positions_to_close = []
        for position_id, position in self.active_positions.items():
            should_close = self.strategy.should_close_position(
                position['entry_price'],
                current_price,
                position['action'],
                position['stop_loss'],
                position['take_profit']
            )
            if should_close:
                positions_to_close.append(position_id)
        
        # Chiudi posizioni
        for position_id in positions_to_close:
            self.close_position(position_id)
    
    def run(self, duration_minutes=None):
        """
        Esegue il trading bot
        
        Args:
            duration_minutes: Durata esecuzione in minuti (None = infinito)
        """
        if not self.connector.connected:
            logger.error("Non connesso a IB Gateway")
            return
        
        logger.info("=== Avvio Agente di Scalping ===")
        logger.info(f"Simbolo: {config.SYMBOL}")
        logger.info(f"Dimensione posizione: {config.POSITION_SIZE}")
        logger.info(f"Target profitto: {config.PROFIT_TARGET * 100:.2f}%")
        logger.info(f"Stop loss: {config.STOP_LOSS * 100:.2f}%")
        
        self.running = True
        start_time = datetime.now()
        
        try:
            while self.running:
                # Verifica durata
                if duration_minutes and (datetime.now() - start_time).total_seconds() / SECONDS_PER_MINUTE > duration_minutes:
                    logger.info("Durata esecuzione completata")
                    break
                
                # Gestisci posizioni esistenti
                self.manage_positions()
                
                # Genera nuovo segnale solo se non abbiamo raggiunto il limite di posizioni
                if len(self.active_positions) < config.MAX_POSITIONS and self.check_risk_limits():
                    signal = self.strategy.generate_signal()
                    if signal:
                        self.open_position(signal)
                
                # Attendi prima del prossimo ciclo
                time.sleep(config.SCALPING_TIMEFRAME)
                
        except KeyboardInterrupt:
            logger.info("Interruzione da utente")
        except Exception as e:
            logger.error(f"Errore durante esecuzione: {e}", exc_info=True)
        finally:
            # Chiudi tutte le posizioni aperte
            logger.info("Chiusura posizioni aperte...")
            for position_id in list(self.active_positions.keys()):
                self.close_position(position_id)
            
            logger.info(f"=== Fine Trading - P&L giornaliero: {self.daily_pnl:.2f} USD ===")
            logger.info(f"Trade eseguiti: {self.daily_trades}")


def main():
    """Funzione principale"""
    agent = ScalpingAgent()
    
    # Connetti a IB Gateway
    if not agent.connect():
        logger.error("Impossibile connettersi a IB Gateway")
        return
    
    try:
        # Esegui trading bot
        # Per test, limita a 60 minuti. Rimuovi il parametro per esecuzione continua
        agent.run(duration_minutes=60)
    finally:
        # Disconnetti
        agent.disconnect()


if __name__ == '__main__':
    main()
