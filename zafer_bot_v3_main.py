#!/usr/bin/env python3
"""
ZAFER BOT v3 - ADVANCED TRADING SYSTEM
🚀 Ultra-Smart Trading Bot with ML, Grid Trading, and Advanced Risk Management

Features:
✅ Machine Learning Predictions
✅ Grid Trading Strategy
✅ Advanced Indicators (Divergence, Fibonacci, Swing Detection)
✅ Portfolio Correlation Filter
✅ Dynamic Position Sizing (Kelly Criterion)
✅ Advanced Risk Management (ATR, Kademeli Kâr Alma)
✅ Database Tracking & Analytics
✅ Multi-Timeframe Analysis
✅ Telegram Notifications
✅ Performance Reporting
"""

import time
import datetime
import requests
import ccxt
import pandas as pd
import ta
import numpy as np
from zafer_config_v3 import *
from zafer_logger_v3 import logger
from zafer_database_v3 import ZaferDatabase
from zafer_ml_prediction_v3 import MLPredictor
from zafer_indicators_v3 import AdvancedIndicators
from zafer_grid_trading_v3 import GridTrading
from zafer_portfolio_optimization_v3 import PortfolioOptimizer

class ZaferBotV3:
    def __init__(self, symbols, initial_balance=INITIAL_BALANCE):
        self.symbols = symbols
        self.balance = initial_balance
        self.initial_balance = initial_balance
        
        self.positions = {symbol: None for symbol in symbols}
        self.price_history = {symbol: [] for symbol in symbols}
        
        self.exchange = ccxt.binance({'enableRateLimit': True})
        self.db = ZaferDatabase(DB_PATH)
        
        self.ml_predictors = {symbol: MLPredictor() for symbol in symbols}
        self.grid_traders = {symbol: GridTrading() for symbol in symbols}
        
        self.daily_pnl = 0.0
        self.total_trades = 0
        self.winning_trades = 0
        
        logger.info(f"🚀 Zafer Bot v3 başlatıldı | Bakiye: {self.balance:.2f} USDT")
        self.send_telegram(f"🚀 *Zafer Bot v3 Aktif*\n💰 Başlangıç Bakiye: {self.balance:.2f} USDT\n📊 Takip Coin: {len(symbols)}")
    
    def send_telegram(self, message):
        """Telegram mesajı gönder"""
        token = TELEGRAM_TOKEN.strip()
        chat_id = TELEGRAM_CHAT_ID.strip()
        if not token or not chat_id:
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            logger.warning(f"⚠️ Telegram hatası: {e}")
    
    def fetch_analysis(self, symbol):
        """Multi-timeframe analiz (1H, 4H, 15M)"""
        try:
            # Main timeframe (1H)
            ohlcv_1h = self.exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
            df_1h = pd.DataFrame(ohlcv_1h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # İndikatörler
            df_1h['rsi'] = ta.momentum.rsi(df_1h['close'], window=RSI_PERIOD)
            macd_ind = ta.trend.MACD(df_1h['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
            df_1h['macd'] = macd_ind.macd()
            df_1h['macd_signal'] = macd_ind.macd_signal()
            
            bb = ta.volatility.BollingerBands(df_1h['close'], window=BB_PERIOD, window_dev=BB_STD)
            df_1h['bb_lower'] = bb.bollinger_lband()
            df_1h['bb_upper'] = bb.bollinger_hband()
            df_1h['bb_middle'] = bb.bollinger_mavg()
            
            df_1h['atr'] = ta.volatility.average_true_range(df_1h['high'], df_1h['low'], df_1h['close'], window=ATR_PERIOD)
            df_1h['vol_sma'] = df_1h['volume'].rolling(window=20).mean()
            
            # Advanced indicators
            df_1h['adx'] = ta.trend.adx(df_1h['high'], df_1h['low'], df_1h['close'], window=14)
            df_1h['ema12'] = ta.trend.ema_indicator(df_1h['close'], window=12)
            df_1h['ema26'] = ta.trend.ema_indicator(df_1h['close'], window=26)
            
            # Secondary timeframe (4H)
            ohlcv_4h = self.exchange.fetch_ohlcv(symbol, timeframe='4h', limit=200)
            df_4h = pd.DataFrame(ohlcv_4h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df_4h['ma50'] = ta.trend.sma_indicator(df_4h['close'], window=50)
            df_4h['ma200'] = ta.trend.sma_indicator(df_4h['close'], window=200)
            
            # Tertiary timeframe (15M)
            ohlcv_15m = self.exchange.fetch_ohlcv(symbol, timeframe='15m', limit=200)
            df_15m = pd.DataFrame(ohlcv_15m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            latest = df_1h.iloc[-1]
            price = float(latest['close'])
            
            # Regime belirle
            regime_bull = float(df_4h['ma50'].iloc[-1]) > float(df_4h['ma200'].iloc[-1])
            
            # Advanced patterns
            divergence = AdvancedIndicators.detect_divergence(df_1h)
            swing = AdvancedIndicators.swing_highs_lows(df_1h)
            sr_levels = AdvancedIndicators.calculate_support_resistance(df_1h)
            fib_levels = AdvancedIndicators.fibonacci_levels(float(df_1h['high'].max()), float(df_1h['low'].min()))
            patterns = AdvancedIndicators.detect_pattern(df_1h)
            
            # ML prediction
            current_features = [
                price,
                float(latest['rsi']),
                float(latest['macd']),
                float(latest['volume']),
                float(latest['close'] - latest['open']),
                float(latest['high'] - latest['low']),
                float(df_1h['close'].mean()),
                float(df_1h['volume'].mean())
            ]
            ml_direction = self.ml_predictors[symbol].predict_direction(current_features)
            
            # Fiyat geçmişi kaydet
            self.price_history[symbol].append(price)
            if len(self.price_history[symbol]) > 100:
                self.price_history[symbol].pop(0)
            
            self.db.log_price(symbol, price, float(latest['rsi']), float(latest['macd']), float(latest['volume']))
            
            return {
                "price": price,
                "rsi": float(latest['rsi']),
                "macd": float(latest['macd']),
                "macd_signal": float(latest['macd_signal']),
                "bb_lower": float(latest['bb_lower']),
                "bb_upper": float(latest['bb_upper']),
                "bb_middle": float(latest['bb_middle']),
                "atr": float(latest['atr']),
                "adx": float(latest['adx']),
                "volume_ok": float(latest['volume']) > (float(latest['vol_sma']) * MIN_VOLUME_MULTIPLIER),
                "regime_bull": regime_bull,
                "ema12": float(latest['ema12']),
                "ema26": float(latest['ema26']),
                "divergence": divergence,
                "swing": swing,
                "sr_levels": sr_levels,
                "fib_levels": fib_levels,
                "patterns": patterns,
                "ml_direction": ml_direction,
                "df_1h": df_1h,
                "df_4h": df_4h,
                "df_15m": df_15m
            }
        except Exception as e:
            logger.error(f"❌ {symbol} analiz hatası: {e}")
            return None
    
    def calculate_position_size(self, capital):
        """Dynamic position sizing"""
        if USE_KELLY_SIZING:
            stats = self.db.get_trade_stats(days=30)
            win_rate = stats['win_rate'] / 100 if stats['win_rate'] > 0 else 0.5
            avg_win = stats['avg_pnl'] if stats['avg_pnl'] > 0 else 100
            avg_loss = abs(stats['worst_trade']) if stats['worst_trade'] < 0 else 50
            
            return PortfolioOptimizer.kelly_sizing(win_rate, avg_win, avg_loss, capital)
        else:
            return capital * MAX_POSITION_SIZE_PERCENT
    
    def process_symbol(self, symbol):
        """Symbol işlemesi (Alım/Satım mantığı)"""
        data = self.fetch_analysis(symbol)
        if not data:
            return
        
        price = data["price"]
        rsi = data["rsi"]
        macd = data["macd"]
        macd_signal = data["macd_signal"]
        atr = data["atr"]
        adx = data["adx"]
        bb_lower = data["bb_lower"]
        volume_ok = data["volume_ok"]
        regime_bull = data["regime_bull"]
        ema12 = data["ema12"]
        ema26 = data["ema26"]
        divergence = data["divergence"]
        swing = data["swing"]
        sr_levels = data["sr_levels"]
        patterns = data["patterns"]
        ml_direction = data["ml_direction"]
        
        pos = self.positions[symbol]
        regime_str = "🐂 BOĞA" if regime_bull else "🐻 AYI"
        
        logger.info(f"[{symbol}] P:{price:.2f} | RSI:{rsi:.1f} | ADX:{adx:.1f} | {regime_str} | ML:{ml_direction}")
        
        # ============ ALIM STRATEJİSİ ============
        if pos is None and len([p for p in self.positions.values() if p]) < MAX_CONCURRENT_POSITIONS:
            buy_type = None
            buy_score = 0
            
            # Strateji 1: Momentum + Trend (MACD + RSI + ADX)
            if regime_bull and macd > macd_signal and rsi < RSI_OVERBOUGHT and volume_ok and adx > 25 and ml_direction == 1:
                buy_type = "🔥 MOMENTUM + ML"
                buy_score = 90
            
            # Strateji 2: Fırsat Avcısı (Divergence + Swing Low)
            elif divergence and divergence['bullish'] and swing and swing['swing_low'] and rsi < RSI_OVERSOLD:
                buy_type = "🎯 DIVERGENCEᴸ + SWING"
                buy_score = 80
            
            # Strateji 3: Fibonacci Rebound
            elif price < sr_levels['support'] and ema12 > ema26 and rsi > 30:
                buy_type = "📐 FIB REBOUND"
                buy_score = 75
            
            # Strateji 4: Pattern Recognition
            elif patterns and (patterns.get('hammer') or patterns.get('engulfing_bull')):
                buy_type = "🕯️ PATTERN"
                buy_score = 70
            
            if buy_type and buy_score >= 70:
                # Position size hesapla
                trade_amount = self.calculate_position_size(self.balance)
                amount_coin = trade_amount / price
                
                # Dinamik stop loss
                dynamic_stop = price - (STOP_LOSS_ATR_MULTIPLIER * atr)
                
                self.positions[symbol] = {
                    "entry_price": price,
                    "avg_price": price,
                    "amount_coin": amount_coin,
                    "total_amount_usdt": trade_amount,
                    "stop_loss_price": dynamic_stop,
                    "dca_count": 0,
                    "max_profit_seen": 0.0,
                    "partial_tp_done": [False] * len(TAKE_PROFIT_LEVELS),
                    "entry_time": time.time(),
                    "buy_type": buy_type,
                    "buy_score": buy_score,
                    "grid_orders": self.grid_traders[symbol].create_grid(symbol, price, trade_amount)
                }
                self.balance -= trade_amount
                self.total_trades += 1
                
                msg = (f"🎯 *[{buy_type} | SCORE: {buy_score}]*\n"
                       f"📌 `{symbol}`\n"
                       f"💵 Entry: `{price:.2f} USDT`\n"
                       f"🛡️ Stop (2xATR): `{dynamic_stop:.2f} USDT`\n"
                       f"📊 RSI: `{rsi:.1f}` | ADX: `{adx:.1f}` | ML: `{ml_direction}`\n"
                       f"💰 Yatırılan: `{trade_amount:.2f} USDT`")
                logger.info(msg)
                self.send_telegram(msg)
        
        # ============ POZİSYON YÖNETİMİ ============
        elif pos:
            avg_price = pos["avg_price"]
            total_amount = pos["total_amount_usdt"]
            amount_coin = pos["amount_coin"]
            pnl_pct = ((price - avg_price) / avg_price) * 100
            
            if pnl_pct > pos["max_profit_seen"]:
                self.positions[symbol]["max_profit_seen"] = pnl_pct
            
            # Parçalı Kâr Alma (Kademeli)
            for i, tp_level in enumerate(TAKE_PROFIT_LEVELS):
                if pnl_pct >= (tp_level * 100) and not pos["partial_tp_done"][i]:
                    sell_amount = amount_coin * PARTIAL_TAKE_PROFIT[i]
                    realized_usdt = sell_amount * price
                    pnl_realized = realized_usdt - (total_amount * PARTIAL_TAKE_PROFIT[i])
                    
                    self.balance += realized_usdt
                    self.positions[symbol]["amount_coin"] -= sell_amount
                    self.positions[symbol]["total_amount_usdt"] -= (total_amount * PARTIAL_TAKE_PROFIT[i])
                    self.positions[symbol]["partial_tp_done"][i] = True
                    
                    # Stop loss güncelle
                    if i == 0:
                        self.positions[symbol]["stop_loss_price"] = avg_price
                    
                    self.daily_pnl += pnl_realized
                    self.winning_trades += 1
                    
                    msg = (f"💰 *[PARÇALI KÂR ALINDI - TP{i+1}]*\n"
                           f"📌 `{symbol}`\n"
                           f"💵 Satış: `{price:.2f} USDT`\n"
                           f"📈 Kâr: `+{pnl_realized:.2f} USDT ({tp_level*100:.0f}%)`\n"
                           f"💰 Güncel Bakiye: `{self.balance:.2f} USDT`")
                    logger.info(msg)
                    self.send_telegram(msg)
            
            # Akıllı DCA
            if pnl_pct < DCA_THRESHOLD and price < sr_levels['support'] and pos["dca_count"] < DCA_MAX_COUNT:
                dca_amount = total_amount * DCA_MULTIPLIER
                if self.balance >= dca_amount:
                    new_coin = dca_amount / price
                    total_coin = amount_coin + new_coin
                    new_total_usdt = total_amount + dca_amount
                    new_avg_price = new_total_usdt / total_coin
                    
                    self.balance -= dca_amount
                    self.positions[symbol]["avg_price"] = new_avg_price
                    self.positions[symbol]["amount_coin"] = total_coin
                    self.positions[symbol]["total_amount_usdt"] = new_total_usdt
                    self.positions[symbol]["dca_count"] += 1
                    self.positions[symbol]["stop_loss_price"] = new_avg_price - (STOP_LOSS_ATR_MULTIPLIER * atr)
                    
                    msg = (f"🛠️ *[AKILLI DCA]*\n"
                           f"📌 `{symbol}`\n"
                           f"📉 Yeni Ortalama: `{new_avg_price:.2f} USDT`\n"
                           f"➕ Eklenen: `{dca_amount:.2f} USDT` ({pos['dca_count']+1}/3)")
                    logger.info(msg)
                    self.send_telegram(msg)
            
            # Grid Trading Kontrol
            grid_orders = self.grid_traders[symbol].check_grid_levels(symbol, price)
            for order in grid_orders:
                logger.info(f"📊 Grid Level Tetiklendi: {symbol} @ {order['price']:.2f}")
            
            # Çıkış Koşulları
            exit_reason = None
            hours_in_trade = (time.time() - pos["entry_time"]) / 3600
            
            # Kademeli Kâr Koruma
            if pos["max_profit_seen"] > 25.0 and pnl_pct < 20.0:
                exit_reason = "🔒 KÂR KORUMA L4 (%20)"
            elif pos["max_profit_seen"] > 15.0 and pnl_pct < 12.0:
                exit_reason = "🔒 KÂR KORUMA L3 (%12)"
            elif pos["max_profit_seen"] > 8.0 and pnl_pct < 5.0:
                exit_reason = "🔒 KÂR KORUMA L2 (%5)"
            
            # ATR Stop Loss
            elif price < pos["stop_loss_price"]:
                exit_reason = f"🔴 ATR STOP ({pos['stop_loss_price']:.2f})"
            
            # Trend Bitişi
            elif pos["buy_type"].startswith("🔥") and macd < macd_signal and pnl_pct > 2.0:
                exit_reason = "📉 TREND BİTİŞİ"
            
            # Reverse Divergence
            elif divergence and divergence['bearish'] and pnl_pct > 3.0:
                exit_reason = "⚠️ BEARISH DIV"
            
            # Zaman Aşımı
            elif hours_in_trade > 48 and abs(pnl_pct) < 2.0:
                exit_reason = "⏰ ZAMAN AŞIMI (48H)"
            
            # Çıkış Gerçekleştir
            if exit_reason:
                current_coin = self.positions[symbol]["amount_coin"]
                return_usdt = current_coin * price
                pnl_usdt = return_usdt - self.positions[symbol]["total_amount_usdt"]
                
                self.balance += return_usdt
                self.daily_pnl += pnl_usdt
                
                msg = (f"🚪 *[POZİSYON KAPATILDI]*\n"
                       f"📌 `{symbol}` ({pos['buy_type']})\n"
                       f"💡 Sebep: `{exit_reason}`\n"
                       f"📊 Entry: `{avg_price:.2f}` | Exit: `{price:.2f}`\n"
                       f"📈 Sonuç: `%{pnl_pct:.2f}` ({pnl_usdt:+.2f} USDT)\n"
                       f"💰 Toplam Bakiye: `{self.balance:.2f} USDT`")
                logger.info(msg)
                self.send_telegram(msg)
                
                self.db.close_trade(symbol, price, exit_reason, pnl_usdt, pnl_pct)
                self.positions[symbol] = None
    
    def generate_daily_report(self):
        """Günlük rapor"""
        stats = self.db.get_trade_stats(days=1)
        roi = ((self.balance - self.initial_balance) / self.initial_balance) * 100
        
        report = (f"📊 *ZAFER BOT v3 - GÜNLÜK RAPOR*\n"
                 f"{'=' * 40}\n"
                 f"📈 İlk Bakiye: `${self.initial_balance:.2f}`\n"
                 f"💰 Güncel Bakiye: `${self.balance:.2f}`\n"
                 f"📊 Günlük P&L: `${self.daily_pnl:+.2f}`\n"
                 f"📈 ROI: `{roi:+.2f}%`\n"
                 f"\n📋 İSTATİSTİKLER:\n"
                 f"• Toplam Trade: `{stats['total_trades']}`\n"
                 f"• Kazanan: `{stats['winning_trades']}` | Kaybeden: `{stats['losing_trades']}`\n"
                 f"• Win Rate: `{stats['win_rate']:.1f}%`\n"
                 f"• Avg Profit: `${stats['avg_pnl']:+.2f}`\n"
                 f"• Best Trade: `${stats['best_trade']:.2f}`\n"
                 f"• Worst Trade: `${stats['worst_trade']:.2f}`\n"
                 f"{'=' * 40}")
        
        logger.info(report)
        self.send_telegram(report)
        self.daily_pnl = 0.0
    
    def run(self, interval_seconds=SCAN_INTERVAL):
        """Bot ana döngüsü"""
        logger.info("=" * 65)
        logger.info("🚀 ZAFER BOT v3 - ADVANCED TRADING SYSTEM")
        logger.info(f"📊 Takip Coin: {len(self.symbols)}")
        logger.info(f"💰 Başlangıç Bakiye: {self.balance:.2f} USDT")
        logger.info("=" * 65)
        
        last_report_time = datetime.datetime.now()
        
        while True:
            try:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                open_positions = len([p for p in self.positions.values() if p])
                logger.info(f"\n[{current_time}] 🔄 Tarama | Açık Pozisyon: {open_positions} | Bakiye: {self.balance:.2f} USDT")
                
                for symbol in self.symbols:
                    try:
                        self.process_symbol(symbol)
                    except Exception as e:
                        logger.error(f"❌ {symbol} işleme hatası: {e}")
                
                # Günlük rapor
                current_time_obj = datetime.datetime.now()
                if (current_time_obj - last_report_time).seconds > 86400:  # 24 saat
                    self.generate_daily_report()
                    last_report_time = current_time_obj
                
                time.sleep(interval_seconds)
            
            except KeyboardInterrupt:
                logger.warning("\n⚠️ Bot durduruldu!")
                self.send_telegram("🛑 *Bot Durduruldu*\n💰 Son Bakiye: ${:.2f}".format(self.balance))
                break
            except Exception as e:
                logger.error(f"❌ Bot hatası: {e}")
                self.send_telegram(f"🚨 *Bot Hatası*\n❌ {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = ZaferBotV3(symbols=SYMBOLS, initial_balance=INITIAL_BALANCE)
    bot.run(interval_seconds=SCAN_INTERVAL)
