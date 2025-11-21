"""
Configurazione per l'agente di scalping IB Gateway
"""

# Parametri di connessione IB Gateway
IB_HOST = '127.0.0.1'
IB_PORT = 4002  # 4002 per IB Gateway paper trading, 7497 per TWS paper trading
IB_CLIENT_ID = 1

# Parametri di trading
SYMBOL = 'EUR.USD'  # Coppia forex per scalping
CONTRACT_TYPE = 'CASH'  # CASH per forex, STK per azioni
EXCHANGE = 'IDEALPRO'  # Exchange per forex

# Parametri scalping
POSITION_SIZE = 20000  # Dimensione posizione in unità base
PROFIT_TARGET = 0.0005  # Target di profitto (0.05% = 5 pips per EUR/USD)
STOP_LOSS = 0.0003  # Stop loss (0.03% = 3 pips per EUR/USD)
MAX_POSITIONS = 3  # Numero massimo di posizioni simultanee
SCALPING_TIMEFRAME = 5  # Timeframe in secondi per analisi

# Parametri indicatori
EMA_FAST = 5  # EMA veloce per signal
EMA_SLOW = 15  # EMA lenta per signal
RSI_PERIOD = 14  # Periodo RSI
RSI_OVERBOUGHT = 70  # Soglia ipercomprato
RSI_OVERSOLD = 30  # Soglia ipervenduto

# Risk management
MAX_DAILY_LOSS = -500  # Perdita massima giornaliera in USD
MAX_DAILY_TRADES = 50  # Numero massimo di trade giornalieri
