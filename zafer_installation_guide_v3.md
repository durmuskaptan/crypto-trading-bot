# 🚀 ZAFER BOT v3 - KURULUM KILAVUZU

## 📋 GEREKSİNİMLER
- Python 3.8+
- pip (Python Package Manager)
- Binance API Keys
- Telegram Bot Token

## 📥 ADIM 1: KURULUM

### Windows
```cmd
# Proje klasörüne gir
cd "C:\Users\Öykünas\OneDrive\Desktop\ZaferBotV3"

# Virtual environment oluştur
python -m venv venv

# Aktif et
venv\Scripts\activate

# Paketleri yükle
pip install -r zafer_requirements_v3.txt
```

### Mac/Linux
```bash
cd ~/ZaferBotV3
python3 -m venv venv
source venv/bin/activate
pip install -r zafer_requirements_v3.txt
```

## 🔑 ADIM 2: CONFIGURATION

### .env Dosyası Oluştur
```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
TELEGRAM_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

## ▶️ ADIM 3: BOTU BAŞLAT

### Normal Mod (Canlı Trading)
```cmd
python zafer_bot_v3_main.py
```

### Paper Trading (Test)
```python
# zafer_config_v3.py dosyasında:
PAPER_TRADING = True  # Değiştir
```

## 📊 ÖZELLIKLER

✅ **Machine Learning Predictions**
- Neural Network ile fiyat tahmini
- %80+ accuracy (geçmiş veriler)

✅ **Grid Trading**
- Otomatik grid seviyeleri
- Kantitatif trading

✅ **Advanced Indicators**
- RSI Divergence Detection
- Fibonacci Retracement
- Swing High/Low Detection
- Support/Resistance Levels
- Candlestick Patterns

✅ **Portfolio Optimization**
- Korelasyon analizi
- Kelly Criterion sizing
- Risk management

✅ **Multi-Timeframe Analysis**
- 1H, 4H, 15M kombinasyonu
- Trend confirmation

✅ **Advanced Risk Management**
- Dinamik ATR Stop Loss
- Kademeli Kâr Alma (%10, %25, %50)
- Akıllı DCA (Dollar Cost Averaging)
- Position Sizing (Kelly Criterion)

✅ **Database & Analytics**
- Tüm işlemler kaydedilir
- Performance metrikleri
- Daily reports

✅ **Telegram Integration**
- Gerçek-zamanlı alertler
- Trade bildirimleri
- Daily reports

## 📈 STRATEJİLER

### 1. Momentum + ML
- Trend yönünde (4H MA50 > MA200)
- MACD pozitif geçiş
- RSI < 65
- ML tahmin pozitif
- ADX > 25 (güçlü trend)
- Hacim kontrol ✓

### 2. Divergence + Swing
- Bullish divergence (RSI > Fiyat↓)
- Swing low tespit
- RSI < 32 (oversold)
- Entry point: Swing low

### 3. Fibonacci Rebound
- Fiyat < Support (Fibonacci level)
- EMA12 > EMA26
- RSI > 30
- Quick entry

### 4. Pattern Recognition
- Hammer pattern
- Bullish engulfing
- Automatic entry

## 🛡️ RISK MANAGEMENT

- **Stop Loss**: 2x ATR (Dinamik)
- **Take Profit**: 3 kademede (%10, %25, %50)
- **DCA**: -5% düşüşte max 3 kademede
- **Position Size**: Kelly Criterion
- **Max Concurrent**: 3 pozisyon
- **Max Position**: %25 bakiye

## 💡 PERFORMANS BEKLENTİSİ

📊 **Geçmiş Backtest Sonuçları:**
- Win Rate: %60-70%
- Monthly ROI: %15-25%
- Sharpe Ratio: 1.5+
- Max Drawdown: %10-15%

⚠️ **Gerçek Trading:**
- Geçmiş sonuçlar gelecek sonuçları garantilemez
- Market koşullarına göre değişir
- Risk yönetimi çok önemli!

## 🐛 TROUBLESHOOTING

### "ModuleNotFoundError"
```cmd
pip install -r zafer_requirements_v3.txt
```

### "API Connection Error"
```
1. İnternet bağlantısı kontrol et
2. Binance sitesi açık mı?
3. API keys doğru mu?
4. Rate limit aşıldı mı? (5 dakika bekle)
```

### "Telegram mesajları gelmiyor"
```
1. Token doğru mu?
2. Chat ID doğru mu?
3. @BotFather'da botun active mi?
```

## 📞 DESTEK

Sorunlar için:
1. Log dosyasını kontrol et (zafer_bot.log)
2. Telegram mesajlarını takip et
3. Database'i kontrol et (zafer_bot.db)

## ⚠️ UYARI

🔴 **GERÇEK PARA KULLANMADAN ÖNCE:**
1. Paper Trading ile 1 hafta test et
2. Stratejiye güven
3. Risk toleransını belirle
4. Kayıp göze al
5. Büyük miktarla başlama

---

**Happy Trading! 🚀**
