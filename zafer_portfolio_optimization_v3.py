import numpy as np
from zafer_logger_v3 import logger

class PortfolioOptimizer:
    """Portfolio Optimizasyonu ve Korelasyon Analizi"""
    
    @staticmethod
    def calculate_correlation(price_histories):
        """Coin'ler arasındaki korelasyonu hesapla"""
        correlations = {}
        symbols = list(price_histories.keys())
        
        for i, symbol1 in enumerate(symbols):
            for symbol2 in symbols[i+1:]:
                if symbol1 in price_histories and symbol2 in price_histories:
                    prices1 = np.array(price_histories[symbol1])
                    prices2 = np.array(price_histories[symbol2])
                    
                    if len(prices1) > 1 and len(prices2) > 1:
                        corr = np.corrcoef(prices1, prices2)[0, 1]
                        correlations[f"{symbol1}-{symbol2}"] = corr
        
        return correlations
    
    @staticmethod
    def should_open_position(symbol, correlations, threshold=0.7):
        """Yüksek korelasyonlu pozisyon açılmalı mı?"""
        # Diğer pozisyonlarla yüksek korelasyon varsa açma
        for pair, corr in correlations.items():
            if symbol in pair and abs(corr) > threshold:
                logger.warning(f'⚠️ {symbol} yüksek korelasyonlu ({corr:.2f})')
                return False
        
        return True
    
    @staticmethod
    def calculate_portfolio_risk(positions, price_history):
        """Portfolio risk değerlendirmesi"""
        total_exposure = sum(p.get('total_amount_usdt', 0) for p in positions.values() if p)
        
        if total_exposure == 0:
            return 0
        
        risk_score = 0
        for symbol, position in positions.items():
            if position:
                exposure_pct = position.get('total_amount_usdt', 0) / total_exposure
                risk_score += exposure_pct
        
        return risk_score
    
    @staticmethod
    def kelly_sizing(win_rate, avg_win, avg_loss, bankroll):
        """Kelly Criterion Position Sizing"""
        if avg_loss == 0:
            return bankroll * 0.02  # Default %2
        
        # Kelly = (Win% * Avg Win - Loss% * Avg Loss) / Avg Win
        win_loss_ratio = avg_win / abs(avg_loss)
        kelly_pct = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        
        # Güvenlik için Kelly'nin %25'ini kullan
        kelly_safe = kelly_pct * 0.25
        kelly_safe = max(0.01, min(0.05, kelly_safe))  # %1 - %5 arasında
        
        return bankroll * kelly_safe