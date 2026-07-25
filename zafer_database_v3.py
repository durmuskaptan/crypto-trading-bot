import sqlite3
import json
from datetime import datetime
from zafer_logger_v3 import logger

class ZaferDatabase:
    def __init__(self, db_path='zafer_bot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Database tabloları oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trades tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                entry_price REAL NOT NULL,
                entry_time TIMESTAMP NOT NULL,
                exit_price REAL,
                exit_time TIMESTAMP,
                entry_reason TEXT,
                exit_reason TEXT,
                amount_coin REAL NOT NULL,
                total_usdt REAL NOT NULL,
                pnl_usdt REAL,
                pnl_percent REAL,
                status TEXT DEFAULT 'OPEN',
                dca_count INTEGER DEFAULT 0,
                max_profit REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily Summary
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                total_trades INTEGER,
                winning_trades INTEGER,
                losing_trades INTEGER,
                total_pnl REAL,
                win_rate REAL,
                best_trade REAL,
                worst_trade REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Price History (Analiz için)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                rsi REAL,
                macd REAL,
                volume REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Strategy Performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                strategy_type TEXT,
                win_rate REAL,
                total_trades INTEGER,
                avg_win REAL,
                avg_loss REAL,
                profit_factor REAL,
                sharpe_ratio REAL,
                max_drawdown REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info('✅ Database başlatıldı')
    
    def open_trade(self, symbol, entry_price, amount_coin, total_usdt, entry_reason):
        """Açılan trade'i kaydet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trades (symbol, entry_price, entry_time, amount_coin, total_usdt, entry_reason, status)
            VALUES (?, ?, ?, ?, ?, ?, 'OPEN')
        ''', (symbol, entry_price, datetime.now(), amount_coin, total_usdt, entry_reason))
        
        trade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f'📊 Trade #{trade_id} açıldı: {symbol} @ {entry_price:.2f}')
        return trade_id
    
    def close_trade(self, symbol, exit_price, exit_reason, pnl_usdt, pnl_percent):
        """Trade'i kapat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE trades 
            SET exit_price=?, exit_time=?, exit_reason=?, pnl_usdt=?, pnl_percent=?, status='CLOSED'
            WHERE symbol=? AND status='OPEN'
            ORDER BY entry_time DESC LIMIT 1
        ''', (exit_price, datetime.now(), exit_reason, pnl_usdt, pnl_percent, symbol))
        
        conn.commit()
        conn.close()
        
        logger.info(f'🚪 {symbol} Trade kapatıldı: {exit_reason} | P&L: {pnl_percent:+.2f}%')
    
    def get_trade_stats(self, days=30):
        """Trade istatistikleri"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl_usdt > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl_usdt < 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl_usdt) as total_pnl,
                AVG(pnl_usdt) as avg_pnl,
                MAX(pnl_usdt) as best_trade,
                MIN(pnl_usdt) as worst_trade
            FROM trades
            WHERE status='CLOSED' AND datetime(exit_time) > datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        result = cursor.fetchone()
        conn.close()
        
        total_trades = result[0] or 0
        wins = result[1] or 0
        losses = result[2] or 0
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': wins,
            'losing_trades': losses,
            'win_rate': win_rate,
            'total_pnl': result[3] or 0,
            'avg_pnl': result[4] or 0,
            'best_trade': result[5] or 0,
            'worst_trade': result[6] or 0
        }
    
    def log_price(self, symbol, price, rsi, macd, volume):
        """Fiyat geçmişi kaydet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_history (symbol, timestamp, price, rsi, macd, volume)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (symbol, datetime.now(), price, rsi, macd, volume))
        
        conn.commit()
        conn.close()