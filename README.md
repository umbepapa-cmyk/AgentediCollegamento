# AgentediCollegamento

Agente di trading automatizzato che si connette con IB Gateway (Interactive Brokers) per eseguire operazioni di scalping remunerative.

## Caratteristiche

- **Connessione IB Gateway**: Si connette automaticamente a Interactive Brokers Gateway
- **Strategia di Scalping**: Implementa una strategia di scalping basata su:
  - EMA (Exponential Moving Average) veloce e lenta
  - RSI (Relative Strength Index)
  - Analisi del momentum
- **Risk Management**: Include protezioni per:
  - Stop Loss automatico
  - Take Profit automatico
  - Limite perdita massima giornaliera
  - Limite numero massimo di trade giornalieri
  - Limite posizioni simultanee
- **Logging Completo**: Registra tutte le operazioni e decisioni di trading

## Requisiti

- Python 3.8 o superiore
- IB Gateway o TWS (Trader Workstation) installato e configurato
- Account Interactive Brokers (paper trading o live)

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/umbepapa-cmyk/AgentediCollegamento.git
cd AgentediCollegamento
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configura IB Gateway:
   - Avvia IB Gateway o TWS
   - Abilita le connessioni API (Configure -> Settings -> API -> Settings)
   - Porta standard: 4002 (paper trading) o 4001 (live trading)
   - Assicurati che "Read-Only API" sia disabilitato
   - Aggiungi 127.0.0.1 agli IP autorizzati

## Configurazione

Modifica `config.py` per personalizzare i parametri:

```python
# Connessione IB Gateway
IB_HOST = '127.0.0.1'
IB_PORT = 4002  # 4002 per paper trading

# Parametri di trading
SYMBOL = 'EUR.USD'  # Coppia forex
POSITION_SIZE = 20000  # Dimensione posizione
PROFIT_TARGET = 0.0005  # Target profitto (0.05%)
STOP_LOSS = 0.0003  # Stop loss (0.03%)
MAX_POSITIONS = 3  # Posizioni simultanee massime

# Risk management
MAX_DAILY_LOSS = -500  # Perdita massima giornaliera (USD)
MAX_DAILY_TRADES = 50  # Trade massimi al giorno
```

## Utilizzo

### Esecuzione Base

```bash
python scalping_agent.py
```

L'agente si connetterà a IB Gateway e inizierà a:
1. Monitorare il mercato in tempo reale
2. Analizzare i prezzi con gli indicatori tecnici
3. Generare segnali di trading
4. Eseguire ordini automaticamente
5. Gestire posizioni con stop loss e take profit

### Esempio di Output

```
2025-11-21 10:30:15 - INFO - Connesso a IB Gateway su 127.0.0.1:4002
2025-11-21 10:30:15 - INFO - Contratto creato per EUR.USD
2025-11-21 10:30:15 - INFO - === Avvio Agente di Scalping ===
2025-11-21 10:30:15 - INFO - Simbolo: EUR.USD
2025-11-21 10:30:15 - INFO - Dimensione posizione: 20000
2025-11-21 10:30:15 - INFO - Target profitto: 0.05%
2025-11-21 10:30:15 - INFO - Stop loss: 0.03%
2025-11-21 10:31:20 - INFO - SEGNALE BUY - EMA Fast: 1.08453, EMA Slow: 1.08421, RSI: 45.32
2025-11-21 10:31:21 - INFO - Ordine market piazzato: BUY 20000 EUR
2025-11-21 10:31:21 - INFO - Posizione aperta: BUY_20251121_103121
2025-11-21 10:31:21 - INFO - Entry: 1.08450, SL: 1.08418, TP: 1.08504
2025-11-21 10:32:45 - INFO - Take Profit raggiunto: 1.08507 >= 1.08504
2025-11-21 10:32:46 - INFO - Ordine market piazzato: SELL 20000 EUR
2025-11-21 10:32:46 - INFO - Posizione chiusa: BUY_20251121_103121
2025-11-21 10:32:46 - INFO - Exit: 1.08507, P&L: 11.40 USD, P&L giornaliero: 11.40 USD
```

## Struttura del Progetto

```
AgentediCollegamento/
├── README.md                 # Documentazione
├── requirements.txt          # Dipendenze Python
├── config.py                 # Configurazione parametri
├── ib_connector.py           # Modulo connessione IB Gateway
├── scalping_strategy.py      # Strategia di scalping
├── scalping_agent.py         # Agente principale
└── scalping_agent.log        # Log delle operazioni
```

## Strategia di Trading

La strategia implementata utilizza:

1. **EMA Cross**: 
   - EMA veloce (5 periodi) e EMA lenta (15 periodi)
   - Segnale BUY quando EMA veloce > EMA lenta
   - Segnale SELL quando EMA veloce < EMA lenta

2. **RSI Filter**:
   - Evita acquisti in zona ipercomprato (RSI > 70)
   - Evita vendite in zona ipervenduto (RSI < 30)

3. **Momentum Confirmation**:
   - Verifica che il prezzo si muova nella direzione del segnale

4. **Risk Management**:
   - Stop Loss: 0.03% (3 pips per EUR/USD)
   - Take Profit: 0.05% (5 pips per EUR/USD)
   - Rapporto rischio/rendimento: 1:1.67

## Sicurezza e Rischi

⚠️ **IMPORTANTE**: 

- Inizia sempre con **paper trading** per testare la strategia
- Il trading automatizzato comporta rischi significativi
- Non investire più di quanto puoi permetterti di perdere
- I risultati passati non garantiscono risultati futuri
- Monitora regolarmente le performance dell'agente
- Assicurati di comprendere i mercati forex prima di fare trading live

## Personalizzazione

### Cambiare Strumento Finanziario

Per tradare azioni invece di forex:

```python
# config.py
SYMBOL = 'AAPL'  # Ticker azione
CONTRACT_TYPE = 'STK'  # Stock
EXCHANGE = 'SMART'  # Smart routing
```

### Modificare Parametri Strategia

Puoi ottimizzare i parametri della strategia:

```python
# config.py
EMA_FAST = 8  # Modifica periodo EMA veloce
EMA_SLOW = 21  # Modifica periodo EMA lenta
RSI_PERIOD = 14  # Modifica periodo RSI
```

## Troubleshooting

### Errore di Connessione

Se ricevi errori di connessione:
1. Verifica che IB Gateway sia avviato
2. Controlla che la porta sia corretta (4002 per paper trading)
3. Assicurati che le connessioni API siano abilitate
4. Verifica che 127.0.0.1 sia autorizzato

### Nessun Segnale Generato

Se non vengono generati segnali:
1. Attendi che si accumuli abbastanza storico prezzi
2. Verifica che il mercato sia aperto
3. Controlla i parametri della strategia
4. Riduci i periodi EMA/RSI per maggiore sensibilità

## Monitoraggio

L'agente scrive tutte le operazioni nel file `scalping_agent.log`. Puoi monitorare in tempo reale:

```bash
tail -f scalping_agent.log
```

## Licenza

Questo progetto è fornito "as-is" per scopi educativi e di ricerca.

## Disclaimer

Questo software è fornito a scopo informativo e educativo. L'autore non è responsabile per eventuali perdite finanziarie derivanti dall'uso di questo software. Il trading comporta rischi e non è adatto a tutti gli investitori.
