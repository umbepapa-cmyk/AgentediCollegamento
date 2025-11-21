#!/usr/bin/env python3
"""
Script di verifica prerequisiti per l'agente di scalping
"""

import sys
import subprocess


def check_python_version():
    """Verifica versione Python"""
    print("Controllo versione Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Richiesto Python 3.8+)")
        return False


def check_dependencies():
    """Verifica dipendenze installate"""
    print("\nControllo dipendenze...")
    
    dependencies = [
        'ib_insync',
        'pandas',
        'numpy',
        'dotenv'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} installato")
        except ImportError:
            print(f"✗ {dep} NON installato")
            all_ok = False
    
    if not all_ok:
        print("\nInstalla le dipendenze mancanti con:")
        print("  pip install -r requirements.txt")
    
    return all_ok


def check_ib_gateway():
    """Fornisce istruzioni per IB Gateway"""
    print("\n" + "="*50)
    print("IMPORTANTE: IB Gateway")
    print("="*50)
    print("""
Per utilizzare questo agente, devi avere:

1. Account Interactive Brokers (paper trading o live)
   → Registrati su: https://www.interactivebrokers.com

2. IB Gateway installato e configurato
   → Download: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php
   
3. API abilitata in IB Gateway:
   - Configure → Settings → API → Settings
   - Enable ActiveX and Socket Clients: ✓
   - Socket Port: 4002 (paper) o 4001 (live)
   - Trusted IP Addresses: 127.0.0.1
   - Read-Only API: ✗ (disabilitato)

4. IB Gateway deve essere AVVIATO prima di eseguire l'agente
""")


def main():
    """Funzione principale"""
    print("="*50)
    print("VERIFICA PREREQUISITI AGENTE DI SCALPING")
    print("="*50)
    
    checks = [
        check_python_version(),
        check_dependencies()
    ]
    
    check_ib_gateway()
    
    print("\n" + "="*50)
    if all(checks):
        print("✓ SISTEMA PRONTO")
        print("="*50)
        print("\nProssimi passi:")
        print("1. Avvia IB Gateway")
        print("2. Esegui test: python test_agent.py")
        print("3. Prova esempio: python example.py")
        print("4. Leggi QUICKSTART.md per istruzioni dettagliate")
        return 0
    else:
        print("✗ SISTEMA NON PRONTO")
        print("="*50)
        print("\nRisolvi i problemi sopra indicati e riprova.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
