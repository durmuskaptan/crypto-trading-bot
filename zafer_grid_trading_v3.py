import numpy as np
from zafer_logger_v3 import logger

class GridTrading:
    """Grid Trading Stratejisi"""
    def __init__(self, grid_levels=10, price_range_percent=5):
        self.grid_levels = grid_levels
        self.price_range_percent = price_range_percent
        self.grid_orders = {}
    
    def create_grid(self, symbol, entry_price, capital):
        """Grid oluştur"""
        # Fiyat aralığını belirle
        lower_price = entry_price * (1 - self.price_range_percent / 100)
        upper_price = entry_price * (1 + self.price_range_percent / 100)
        
        # Grid seviyeleri
        grid_prices = np.linspace(lower_price, upper_price, self.grid_levels)
        order_size = capital / self.grid_levels
        
        self.grid_orders[symbol] = []
        
        for i, price in enumerate(grid_prices):
            if i == 0:  # İlk sipariş (En düşük)
                order_type = 'BUY'
            elif i == len(grid_prices) - 1:  # Son sipariş (En yüksek)
                order_type = 'SELL'
            else:
                order_type = 'BUY' if i < len(grid_prices) / 2 else 'SELL'
            
            self.grid_orders[symbol].append({
                'price': price,
                'order_size': order_size,
                'type': order_type,
                'executed': False
            })
        
        logger.info(f'📊 {symbol} Grid oluşturuldu: {len(self.grid_orders[symbol])} level')
        return self.grid_orders[symbol]
    
    def check_grid_levels(self, symbol, current_price):
        """Grid seviyelerini kontrol et"""
        if symbol not in self.grid_orders:
            return []
        
        triggered_orders = []
        
        for order in self.grid_orders[symbol]:
            if not order['executed']:
                # Fiyat grid seviyesine ulaştı mı?
                if abs(current_price - order['price']) / order['price'] < 0.005:  # %0.5 tolerans
                    order['executed'] = True
                    triggered_orders.append(order)
        
        return triggered_orders
    
    def reset_grid(self, symbol):
        """Grid'i sıfırla"""
        if symbol in self.grid_orders:
            for order in self.grid_orders[symbol]:
                order['executed'] = False
            logger.info(f'🔄 {symbol} Grid sıfırlandı')