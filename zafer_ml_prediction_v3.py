import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from zafer_logger_v3 import logger
import warnings
warnings.filterwarnings('ignore')

class MLPredictor:
    """Machine Learning ile fiyat tahmini"""
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=100, random_state=42)
        self.is_trained = False
    
    def prepare_features(self, df):
        """Feature hazırlığı"""
        if len(df) < 20:
            return None
        
        features = []
        for i in range(len(df) - 20):
            window = df.iloc[i:i+20]
            feature_row = [
                float(window['close'].iloc[-1]),
                float(window['rsi'].iloc[-1]),
                float(window['macd'].iloc[-1]),
                float(window['volume'].iloc[-1]),
                float(window['close'].iloc[-1] - window['open'].iloc[-1]),  # Body
                float(window['high'].iloc[-1] - window['low'].iloc[-1]),     # Range
                float(window['close'].mean()),  # MA20
                float(window['volume'].mean())
            ]
            features.append(feature_row)
        
        return np.array(features) if features else None
    
    def train(self, df):
        """Model eğit"""
        X = self.prepare_features(df)
        if X is None or len(X) < 5:
            logger.warning('⚠️ ML training için yetersiz veri')
            return False
        
        try:
            X_scaled = self.scaler.fit_transform(X)
            y = df['close'].iloc[20:len(df)].values
            
            self.model.fit(X_scaled, y)
            self.is_trained = True
            logger.info('✅ ML Model eğitildi')
            return True
        except Exception as e:
            logger.error(f'❌ ML eğitim hatası: {e}')
            return False
    
    def predict_direction(self, current_features):
        """Fiyat yönünü tahmin et (-1: Düşüş, 0: Yatay, 1: Yükseliş)"""
        if not self.is_trained:
            return 0
        
        try:
            feature_array = np.array([current_features])
            feature_scaled = self.scaler.transform(feature_array)
            prediction = self.model.predict(feature_scaled)[0]
            
            current_price = current_features[0]
            change_pct = ((prediction - current_price) / current_price) * 100
            
            if change_pct > 1.0:
                return 1  # Yükseliş
            elif change_pct < -1.0:
                return -1  # Düşüş
            else:
                return 0  # Yatay
        except:
            return 0
    
    def get_prediction_confidence(self, current_features):
        """Tahmin güvenilirliği (0-100)"""
        if not self.is_trained:
            return 0
        
        try:
            return abs(self.model.score(self.scaler.transform([current_features]), [current_features[0]])) * 100
        except:
            return 0