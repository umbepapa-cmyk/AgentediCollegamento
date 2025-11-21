"""
Test per verificare l'importazione e la struttura dei moduli
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Testa che tutti i moduli possano essere importati"""
    try:
        import config
        logger.info("✓ config.py importato correttamente")
        
        from ib_connector import IBConnector
        logger.info("✓ ib_connector.py importato correttamente")
        
        from scalping_strategy import ScalpingStrategy
        logger.info("✓ scalping_strategy.py importato correttamente")
        
        from scalping_agent import ScalpingAgent
        logger.info("✓ scalping_agent.py importato correttamente")
        
        return True
    except Exception as e:
        logger.error(f"✗ Errore import: {e}")
        return False


def test_config():
    """Testa che i parametri di configurazione siano validi"""
    try:
        import config
        
        assert hasattr(config, 'IB_HOST'), "IB_HOST mancante"
        assert hasattr(config, 'IB_PORT'), "IB_PORT mancante"
        assert hasattr(config, 'SYMBOL'), "SYMBOL mancante"
        assert hasattr(config, 'POSITION_SIZE'), "POSITION_SIZE mancante"
        assert hasattr(config, 'PROFIT_TARGET'), "PROFIT_TARGET mancante"
        assert hasattr(config, 'STOP_LOSS'), "STOP_LOSS mancante"
        
        assert config.PROFIT_TARGET > 0, "PROFIT_TARGET deve essere positivo"
        assert config.STOP_LOSS > 0, "STOP_LOSS deve essere positivo"
        assert config.POSITION_SIZE > 0, "POSITION_SIZE deve essere positivo"
        
        logger.info("✓ Configurazione valida")
        return True
    except AssertionError as e:
        logger.error(f"✗ Errore configurazione: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Errore: {e}")
        return False


def test_strategy():
    """Testa la strategia di scalping"""
    try:
        from scalping_strategy import ScalpingStrategy
        
        strategy = ScalpingStrategy(ema_fast=5, ema_slow=15, rsi_period=14)
        
        # Aggiungi prezzi di test
        test_prices = [1.0850, 1.0852, 1.0855, 1.0857, 1.0860,
                       1.0862, 1.0865, 1.0867, 1.0870, 1.0872,
                       1.0875, 1.0877, 1.0880, 1.0882, 1.0885,
                       1.0887, 1.0890, 1.0892, 1.0895, 1.0897,
                       1.0900, 1.0902, 1.0905, 1.0907, 1.0910,
                       1.0912, 1.0915, 1.0917, 1.0920, 1.0922]
        
        for price in test_prices:
            strategy.add_price(price)
        
        # Calcola indicatori
        ema_fast = strategy.calculate_ema(strategy.price_history, 5)
        ema_slow = strategy.calculate_ema(strategy.price_history, 15)
        rsi = strategy.calculate_rsi(strategy.price_history, 14)
        
        assert ema_fast is not None, "EMA fast non calcolata"
        assert ema_slow is not None, "EMA slow non calcolata"
        assert rsi is not None, "RSI non calcolato"
        
        logger.info(f"✓ Strategia funzionante - EMA Fast: {ema_fast:.5f}, EMA Slow: {ema_slow:.5f}, RSI: {rsi:.2f}")
        
        # Test calcolo stop loss e take profit
        entry_price = 1.0900
        sl_buy = strategy.calculate_stop_loss(entry_price, 'BUY', 0.0003)
        tp_buy = strategy.calculate_take_profit(entry_price, 'BUY', 0.0005)
        
        assert sl_buy < entry_price, "Stop loss BUY deve essere sotto entry"
        assert tp_buy > entry_price, "Take profit BUY deve essere sopra entry"
        
        logger.info(f"✓ Stop Loss/Take Profit - Entry: {entry_price:.5f}, SL: {sl_buy:.5f}, TP: {tp_buy:.5f}")
        
        return True
    except AssertionError as e:
        logger.error(f"✗ Errore strategia: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Errore: {e}")
        return False


def test_connector_structure():
    """Testa la struttura del connector (senza connessione reale)"""
    try:
        from ib_connector import IBConnector
        
        connector = IBConnector(host='127.0.0.1', port=4002, client_id=1)
        
        assert hasattr(connector, 'connect'), "Metodo connect mancante"
        assert hasattr(connector, 'disconnect'), "Metodo disconnect mancante"
        assert hasattr(connector, 'create_forex_contract'), "Metodo create_forex_contract mancante"
        assert hasattr(connector, 'place_market_order'), "Metodo place_market_order mancante"
        assert hasattr(connector, 'get_market_price'), "Metodo get_market_price mancante"
        
        # Test creazione contratto
        contract = connector.create_forex_contract('EUR.USD', 'IDEALPRO')
        assert contract.symbol == 'EUR', "Simbolo contratto non corretto"
        assert contract.currency == 'USD', "Valuta contratto non corretta"
        assert contract.secType == 'CASH', "Tipo contratto non corretto"
        
        logger.info("✓ IBConnector struttura valida")
        return True
    except AssertionError as e:
        logger.error(f"✗ Errore connector: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Errore: {e}")
        return False


def test_agent_structure():
    """Testa la struttura dell'agente (senza connessione reale)"""
    try:
        from scalping_agent import ScalpingAgent
        
        agent = ScalpingAgent()
        
        assert hasattr(agent, 'connect'), "Metodo connect mancante"
        assert hasattr(agent, 'disconnect'), "Metodo disconnect mancante"
        assert hasattr(agent, 'run'), "Metodo run mancante"
        assert hasattr(agent, 'check_risk_limits'), "Metodo check_risk_limits mancante"
        assert hasattr(agent, 'open_position'), "Metodo open_position mancante"
        assert hasattr(agent, 'close_position'), "Metodo close_position mancante"
        
        # Test risk limits
        agent.daily_pnl = 0
        agent.daily_trades = 0
        assert agent.check_risk_limits() == True, "Risk limits dovrebbero essere OK"
        
        agent.daily_pnl = -600  # Oltre il limite
        assert agent.check_risk_limits() == False, "Risk limits dovrebbero bloccare trading"
        
        logger.info("✓ ScalpingAgent struttura valida")
        return True
    except AssertionError as e:
        logger.error(f"✗ Errore agent: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Errore: {e}")
        return False


def main():
    """Esegue tutti i test"""
    logger.info("=== Test Agente di Scalping ===\n")
    
    tests = [
        ("Import moduli", test_imports),
        ("Configurazione", test_config),
        ("Strategia di scalping", test_strategy),
        ("Struttura IBConnector", test_connector_structure),
        ("Struttura ScalpingAgent", test_agent_structure),
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"\nTest: {name}")
        logger.info("-" * 50)
        result = test_func()
        results.append((name, result))
        logger.info("")
    
    # Riepilogo
    logger.info("\n" + "=" * 50)
    logger.info("RIEPILOGO TEST")
    logger.info("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info(f"\nRisultato: {passed}/{total} test passati")
    
    if passed == total:
        logger.info("\n✓ Tutti i test sono passati! L'agente è pronto per l'uso.")
        logger.info("\nPer utilizzare l'agente:")
        logger.info("1. Avvia IB Gateway o TWS")
        logger.info("2. Esegui: python scalping_agent.py")
        return 0
    else:
        logger.error("\n✗ Alcuni test sono falliti. Correggi gli errori prima di usare l'agente.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
