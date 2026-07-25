import numpy as np
import pandas as pd
import ta
from zafer_logger_v3 import logger

class AdvancedIndicators:
    """İleri teknik indikatörler"""
    
    @staticmethod
    def fibonacci_levels(high, low):
        """Fibonacci Retracement Seviyeleri"""
        diff = high - low
        levels = {
            '0%': high,
            '23.6%': high - diff * 0.236,
            '38.2%': high - diff * 0.382,
            '50%': high - diff * 0.5,
            '61.8%': high - diff * 0.618,
            '78.6%': high - diff * 0.786,
            '100%': low
        }
        return levels
    
    @staticmethod
    def detect_divergence(df):
        """RSI Divergence Algıla"""
        if len(df) < 10:
            return None
        
        rsi = df['rsi'].values
        close = df['close'].values
        
        # Bullish Divergence: Fiyat düşüyor, RSI yükseliyor
        bullish_div = (close[-1] < close[-2]) and (rsi[-1] > rsi[-2])
        
        # Bearish Divergence: Fiyat yükseliyor, RSI düşüyor
        bearish_div = (close[-1] > close[-2]) and (rsi[-1] < rsi[-2])
        
        return {'bullish': bullish_div, 'bearish': bearish_div}
    
    @staticmethod
    def swing_highs_lows(df, period=5):
        """Swing High/Low Tespit Et"""
        if len(df) < period * 2:
            return None
        
        close = df['close'].values
        swing_high = False
        swing_low = False
        
        current_idx = len(close) - 1
        if current_idx >= period:
            # Swing High
            is_swing_high = close[current_idx] > max(close[current_idx-period:current_idx])
            swing_high = is_swing_high
            
            # Swing Low
            is_swing_low = close[current_idx] < min(close[current_idx-period:current_idx])
            swing_low = is_swing_low
        
        return {'swing_high': swing_high, 'swing_low': swing_low}
    
    @staticmethod
    def calculate_support_resistance(df, lookback=50):
        """Support ve Resistance seviyeleri"""
        if len(df) < lookback:
            return None
        
        recent = df['close'].tail(lookback)
        support = recent.min()
        resistance = recent.max()
        middle = (support + resistance) / 2
        
        return {
            'support': support,
            'resistance': resistance,
            'middle': middle,
            'pivot': (resistance + support) / 2
        }
    
    @staticmethod
    def calculate_vpt(df):
        """Volume Price Trend"""
        close_change = df['close'].diff()
        vpt = (close_change / df['close'].shift(1)) * df['volume']
        return vpt.cumsum().iloc[-1]
    
    @staticmethod
    def calculate_obv(df):
        """On Balance Volume"""
        obv = [0]
        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i-1]:
                obv.append(obv[-1] + df['volume'].iloc[i])
            elif df['close'].iloc[i] < df['close'].iloc[i-1]:
                obv.append(obv[-1] - df['volume'].iloc[i])
            else:
                obv.append(obv[-1])
        return obv[-1]
    
    @staticmethod
    def calculate_adx(df, period=14):
        """Average Directional Index"""
        adx = ta.trend.adx(df['high'], df['low'], df['close'], length=period)
        return float(adx.iloc[-1]) if len(adx) > 0 else 0
    
    @staticmethod
    def detect_pattern(df):
        """Candlestick Pattern Deteksiyonu"""
        if len(df) < 3:
            return None
        
        o, h, l, c = df['open'].iloc[-3:].values, df['high'].iloc[-3:].values, df['low'].iloc[-3:].values, df['close'].iloc[-3:].values
        
        patterns = {
            'hammer': (c[-1] > o[-1]) and ((o[-1] - l[-1]) > 2 * (h[-1] - c[-1])),
            'shooting_star': (c[-1] < o[-1]) and ((h[-1] - o[-1]) > 2 * (c[-1] - l[-1])),
            'engulfing_bull': (c[-2] < o[-2]) and (c[-1] > o[-1]) and (c[-1] > o[-2]),
            'engulfing_bear': (c[-2] > o[-2]) and (c[-1] < o[-1]) and (c[-1] < o[-2]),
            'three_white_soldiers': (c[-1] > c[-2] > c[-3]) and (o[-1] > o[-2] > o[-3]),
            'three_black_crows': (c[-1] < c[-2] < c[-3]) and (o[-1] < o[-2] < o[-3])
        }
        
        return patterns