"""
Esempio di utilizzo dell'agente di scalping
"""

from scalping_agent import ScalpingAgent
import logging

# Configura logging per vedere i dettagli
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Esempio di utilizzo base"""
    
    # Crea l'agente
    agent = ScalpingAgent()
    
    # Connetti a IB Gateway
    logger.info("Connessione a IB Gateway...")
    if not agent.connect():
        logger.error("Impossibile connettersi. Assicurati che IB Gateway sia avviato.")
        return
    
    logger.info("Connessione riuscita!")
    
    try:
        # Opzione 1: Esegui per un tempo limitato (es. 30 minuti per test)
        logger.info("Avvio trading per 30 minuti...")
        agent.run(duration_minutes=30)
        
        # Opzione 2: Esegui continuamente (decommentare per uso reale)
        # logger.info("Avvio trading continuo...")
        # agent.run()
        
    except KeyboardInterrupt:
        logger.info("Interruzione da utente (Ctrl+C)")
    except Exception as e:
        logger.error(f"Errore: {e}", exc_info=True)
    finally:
        # Disconnetti
        logger.info("Disconnessione...")
        agent.disconnect()
        logger.info("Completato!")


if __name__ == '__main__':
    main()
