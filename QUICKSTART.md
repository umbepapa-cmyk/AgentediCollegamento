# Guida Rapida - Agente di Scalping IB Gateway

## Setup Iniziale (5 minuti)

### 1. Installa IB Gateway

1. Scarica IB Gateway da: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php
2. Installa e configura con le tue credenziali Interactive Brokers
3. **Importante**: Usa prima l'account di paper trading per testare

### 2. Configura IB Gateway per API

1. Avvia IB Gateway
2. Vai su **Configure → Settings → API → Settings**
3. Configura:
   - ✓ Enable ActiveX and Socket Clients
   - ✓ Socket port: **4002** (per paper trading)
   - ✓ Trusted IP addresses: **127.0.0.1**
   - ✗ Read-Only API: **DISABILITATO**
4. Clicca "OK" e riavvia IB Gateway se richiesto

### 3. Installa il Software

```bash
# Clona il repository
git clone https://github.com/umbepapa-cmyk/AgentediCollegamento.git
cd AgentediCollegamento

# Installa dipendenze
pip install -r requirements.txt
```

## Primo Test (2 minuti)

### Test di Connessione

```bash
# Esegui i test per verificare che tutto funzioni
python test_agent.py
```

Dovresti vedere:
```
✓ PASS: Import moduli
✓ PASS: Configurazione
✓ PASS: Strategia di scalping
✓ PASS: Struttura IBConnector
✓ PASS: Struttura ScalpingAgent

Risultato: 5/5 test passati
```

### Test con IB Gateway

```bash
# Esegui l'esempio (30 minuti di trading simulato)
python example.py
```

## Configurazione Base

Modifica `config.py` per i tuoi parametri:

```python
# Quanto vuoi investire per trade?
POSITION_SIZE = 20000  # Unità (es. 20,000 EUR per EUR/USD)

# Quanto vuoi guadagnare per trade?
PROFIT_TARGET = 0.0005  # 0.05% = circa 5 pips su EUR/USD

# Quanto sei disposto a perdere per trade?
STOP_LOSS = 0.0003  # 0.03% = circa 3 pips su EUR/USD

# Quanti trade contemporanei?
MAX_POSITIONS = 3  # Massimo 3 posizioni aperte insieme

# Protezioni giornaliere
MAX_DAILY_LOSS = -500  # Ferma trading se perdi 500 USD in un giorno
MAX_DAILY_TRADES = 50  # Massimo 50 trade al giorno
```

## Avvio Trading

### Per Paper Trading (Consigliato per Iniziare)

1. **Avvia IB Gateway** con account paper trading
2. **Configura porta** 4002 in `config.py`
3. **Esegui**:
   ```bash
   python scalping_agent.py
   ```

### Per Live Trading (Solo Dopo Test Estensivi)

1. **Avvia IB Gateway** con account live
2. **Cambia porta** a 4001 in `config.py`:
   ```python
   IB_PORT = 4001  # Live trading
   ```
3. **RIDUCI position size** per iniziare:
   ```python
   POSITION_SIZE = 1000  # Inizia piccolo!
   ```
4. **Esegui**:
   ```bash
   python scalping_agent.py
   ```

## Monitoraggio

### Log in Tempo Reale

```bash
# In un altro terminale
tail -f scalping_agent.log
```

Vedrai:
- 📊 Segnali di trading generati
- 💰 Ordini eseguiti
- 📈 Posizioni aperte/chiuse
- 💵 Profitti e perdite

### Stop del Trading

Premi **Ctrl+C** nel terminale dove sta girando l'agente. 

L'agente chiuderà automaticamente tutte le posizioni aperte prima di terminare.

## Sicurezza e Best Practices

### ✓ Cose da FARE

- ✓ Inizia con paper trading
- ✓ Testa per almeno 1 settimana prima di andare live
- ✓ Monitora i log quotidianamente
- ✓ Inizia con position size piccole
- ✓ Imposta MAX_DAILY_LOSS conservativo
- ✓ Tieni IB Gateway sempre aggiornato

### ✗ Cose da NON fare

- ✗ Non andare live senza testare in paper trading
- ✗ Non investire più di quanto puoi perdere
- ✗ Non lasciare girare l'agente senza monitoraggio
- ✗ Non disabilitare i limiti di rischio
- ✗ Non aumentare position size troppo velocemente

## Risoluzione Problemi

### "Errore connessione IB Gateway"

- ✓ IB Gateway è avviato?
- ✓ Porta corretta? (4002 per paper, 4001 per live)
- ✓ API abilitata nelle impostazioni?
- ✓ 127.0.0.1 autorizzato nelle Trusted IPs?

### "Nessun segnale generato"

- ✓ Il mercato è aperto?
- ✓ Hai aspettato almeno 2-3 minuti?
- ✓ I parametri strategia sono troppo restrittivi?

### "Ordini rifiutati"

- ✓ Hai fondi sufficienti nell'account?
- ✓ Position size è compatibile con il tuo account?
- ✓ Il mercato è aperto per lo strumento che stai tradando?

## Supporto

Per problemi o domande:
1. Controlla `scalping_agent.log` per errori dettagliati
2. Verifica la configurazione con `python test_agent.py`
3. Consulta la documentazione completa in `README.md`

## Prossimi Passi

Dopo aver familiarizzato con il sistema:

1. **Ottimizza parametri**: Testa diversi valori di EMA, RSI, profit target
2. **Analizza performance**: Traccia il P&L per identificare pattern
3. **Espandi strumenti**: Aggiungi altri forex o azioni
4. **Migliora strategia**: Implementa filtri aggiuntivi o indicatori

Buon trading! 📈
