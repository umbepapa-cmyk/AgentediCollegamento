"""
Strategia di scalping per forex trading
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ScalpingStrategy:
    """Implementa una strategia di scalping basata su EMA e momentum"""
    
    def __init__(self, ema_fast=5, ema_slow=15, rsi_period=14):
        """
        Inizializza la strategia
        
        Args:
            ema_fast: Periodo EMA veloce
            ema_slow: Periodo EMA lenta
            rsi_period: Periodo RSI
        """
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.rsi_period = rsi_period
        self.price_history = []
        self.max_history = max(ema_slow, rsi_period) * 2
        
    def add_price(self, price):
        """
        Aggiunge un prezzo alla history
        
        Args:
            price: Prezzo corrente
        """
        self.price_history.append(price)
        # Mantieni solo gli ultimi max_history prezzi
        if len(self.price_history) > self.max_history:
            self.price_history = self.price_history[-self.max_history:]
    
    def calculate_ema(self, data, period):
        """
        Calcola EMA (Exponential Moving Average)
        
        Args:
            data: Serie di prezzi
            period: Periodo
            
        Returns:
            EMA value
        """
        if len(data) < period:
            return None
        
        df = pd.Series(data)
        ema = df.ewm(span=period, adjust=False).mean()
        return ema.iloc[-1]
    
    def calculate_rsi(self, data, period):
        """
        Calcola RSI (Relative Strength Index)
        
        Args:
            data: Serie di prezzi
            period: Periodo
            
        Returns:
            RSI value
        """
        if len(data) < period + 1:
            return None
        
        df = pd.Series(data)
        delta = df.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1]
    
    def generate_signal(self):
        """
        Genera segnale di trading
        
        Returns:
            'BUY', 'SELL', o None
        """
        if len(self.price_history) < self.max_history:
            return None
        
        # Calcola indicatori
        ema_fast = self.calculate_ema(self.price_history, self.ema_fast)
        ema_slow = self.calculate_ema(self.price_history, self.ema_slow)
        rsi = self.calculate_rsi(self.price_history, self.rsi_period)
        
        if ema_fast is None or ema_slow is None or rsi is None:
            return None
        
        # Logica di trading
        # BUY: EMA veloce sopra EMA lenta E RSI < 70 (non ipercomprato)
        if ema_fast > ema_slow and rsi < 70:
            # Verifica momentum positivo
            if self.price_history[-1] > self.price_history[-2]:
                logger.info(f"SEGNALE BUY - EMA Fast: {ema_fast:.5f}, EMA Slow: {ema_slow:.5f}, RSI: {rsi:.2f}")
                return 'BUY'
        
        # SELL: EMA veloce sotto EMA lenta E RSI > 30 (non ipervenduto)
        elif ema_fast < ema_slow and rsi > 30:
            # Verifica momentum negativo
            if self.price_history[-1] < self.price_history[-2]:
                logger.info(f"SEGNALE SELL - EMA Fast: {ema_fast:.5f}, EMA Slow: {ema_slow:.5f}, RSI: {rsi:.2f}")
                return 'SELL'
        
        return None
    
    def calculate_stop_loss(self, entry_price, action, stop_loss_pct=0.0003):
        """
        Calcola il livello di stop loss
        
        Args:
            entry_price: Prezzo di entrata
            action: 'BUY' o 'SELL'
            stop_loss_pct: Percentuale stop loss
            
        Returns:
            Prezzo stop loss
        """
        if action == 'BUY':
            return entry_price * (1 - stop_loss_pct)
        else:  # SELL
            return entry_price * (1 + stop_loss_pct)
    
    def calculate_take_profit(self, entry_price, action, profit_pct=0.0005):
        """
        Calcola il livello di take profit
        
        Args:
            entry_price: Prezzo di entrata
            action: 'BUY' o 'SELL'
            profit_pct: Percentuale profitto
            
        Returns:
            Prezzo take profit
        """
        if action == 'BUY':
            return entry_price * (1 + profit_pct)
        else:  # SELL
            return entry_price * (1 - profit_pct)
    
    def should_close_position(self, entry_price, current_price, action, stop_loss, take_profit):
        """
        Determina se chiudere una posizione
        
        Args:
            entry_price: Prezzo di entrata
            current_price: Prezzo corrente
            action: 'BUY' o 'SELL'
            stop_loss: Livello stop loss
            take_profit: Livello take profit
            
        Returns:
            True se la posizione deve essere chiusa
        """
        if action == 'BUY':
            if current_price <= stop_loss:
                logger.info(f"Stop Loss raggiunto: {current_price:.5f} <= {stop_loss:.5f}")
                return True
            if current_price >= take_profit:
                logger.info(f"Take Profit raggiunto: {current_price:.5f} >= {take_profit:.5f}")
                return True
        else:  # SELL
            if current_price >= stop_loss:
                logger.info(f"Stop Loss raggiunto: {current_price:.5f} >= {stop_loss:.5f}")
                return True
            if current_price <= take_profit:
                logger.info(f"Take Profit raggiunto: {current_price:.5f} <= {take_profit:.5f}")
                return True
        
        return False
