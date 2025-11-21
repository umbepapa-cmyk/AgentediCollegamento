# Agente di Collegamento

Agente di trading automatico che si connette a Interactive Brokers Gateway ed esegue operazioni di scalping.

## Caratteristiche

- **Connessione IB Gateway**: Si connette a Interactive Brokers Gateway per l'esecuzione di operazioni
- **Strategia di Scalping**: Implementa una strategia di scalping automatizzata con:
  - Target di profitto configurabile
  - Stop loss configurabile
  - Dimensione posizione personalizzabile
- **Gestione del rischio**: Chiusura automatica delle posizioni al raggiungimento degli obiettivi
- **Logging completo**: Tracciamento dettagliato di tutte le operazioni

## Prerequisiti

- Python 3.8 o superiore
- IB Gateway o TWS (Trader Workstation) in esecuzione
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

3. Configura le variabili d'ambiente:
```bash
cp .env.example .env
```

Modifica il file `.env` con i tuoi parametri:
- `IB_HOST`: Indirizzo IP del Gateway (default: 127.0.0.1)
- `IB_PORT`: Porta del Gateway (4002 per paper trading, 4001 per live)
- `IB_CLIENT_ID`: ID cliente univoco
- `SYMBOL`: Coppia di valute da tradare (es. EUR.USD)
- `PROFIT_TARGET`: Target di profitto in unità di prezzo
- `STOP_LOSS`: Stop loss in unità di prezzo
- `POSITION_SIZE`: Dimensione della posizione

## Utilizzo

### Avvio dell'agente

```bash
python -m src.agent
```

### Arresto dell'agente

Premi `Ctrl+C` per arrestare l'agente in modo sicuro. L'agente chiuderà automaticamente eventuali posizioni aperte prima di disconnettersi.

## Configurazione IB Gateway

Prima di eseguire l'agente, assicurati che IB Gateway sia:
1. In esecuzione sulla porta configurata (default: 4002 per paper trading)
2. Configurato per accettare connessioni API
3. Con l'opzione "Read-Only API" disabilitata se vuoi eseguire ordini

## Struttura del progetto

```
AgentediCollegamento/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Applicazione principale
│   ├── config.py             # Gestione configurazione
│   ├── ib_connection.py      # Modulo di connessione IB Gateway
│   └── scalping_strategy.py  # Logica strategia di scalping
├── requirements.txt          # Dipendenze Python
├── .env.example             # Esempio configurazione
├── .gitignore
└── README.md
```

## Strategia di Scalping

La strategia implementata:
1. Monitora il mercato in tempo reale
2. Entra in posizione quando lo spread bid-ask è favorevole
3. Esce dalla posizione quando:
   - Il target di profitto viene raggiunto
   - Lo stop loss viene attivato
   - L'agente viene arrestato

## Avvertenze

⚠️ **IMPORTANTE**: 
- Questo software è fornito a scopo educativo
- Il trading comporta rischi significativi
- Testa sempre con un account paper trading prima di utilizzare denaro reale
- Non ci assumiamo responsabilità per eventuali perdite finanziarie

## Licenza

Questo progetto è distribuito sotto licenza MIT.
