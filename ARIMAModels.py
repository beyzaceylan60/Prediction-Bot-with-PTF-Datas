import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from pymongo import MongoClient
import joblib

#https://seffaflik.epias.com.tr/electricity/electricity-markets/day-ahead-market-dam/market-clearing-price-mcp
# MongoDB'ye bağlanma
client = MongoClient('localhost', 27017)
db = client['PTF']  # Veritabanı adını değiştirin
collection = db['ptf']  # Koleksiyon adını değiştirin

# Verileri çekme ve DataFrame'e dönüştürme
data_from_mongodb = list(collection.find())  # Verileri çekme, uygun şekilde değiştirin
df = pd.DataFrame(data_from_mongodb)

# Tarih ve Saat sütunlarını birleştirme
df['Tarih_Saat'] = pd.to_datetime(df['Tarih'] + ' ' + df['Saat'])

# Verileri zaman serisi formatına getirme
df.set_index('Tarih_Saat', inplace=True)

# Eğitim ve test verilerini ayırma
train_ratio = 0.9
train_size = int(train_ratio * len(df))
train_data = df[:train_size]
test_data = df[train_size:]

# Otomatik parametre seçimi (pmdarima)
#TL için
model_tl = auto_arima(train_data['PTF (TL/MWh)'], trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
print("Auto ARIMA Model Özeti:")
print(model_tl.summary())
#USD için
model_usd = auto_arima(train_data['PTF (USD/MWh)'], trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
print("Auto ARIMA Model Özeti:")
print(model_usd.summary())
#EUR için
model_eur = auto_arima(train_data['PTF (EUR/MWh)'], trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
print("Auto ARIMA Model Özeti:")
print(model_eur.summary())

# ARIMA modelini eğitme
    # TL için
p, d, q = 5, 1, 1
model_tl = ARIMA(train_data['PTF (TL/MWh)'], order=(p, d, q))
model_fit_tl = model_tl.fit()

# Modeli kaydetme
joblib.dump(model_fit_tl, 'model_tl.pkl')

    # USD için
p, d, q = 4, 1, 3 
model_usd = ARIMA(train_data['PTF (USD/MWh)'], order=(p, d, q))
model_fit_usd = model_usd.fit()

# Modeli kaydetme
joblib.dump(model_fit_usd, 'model_usd.pkl')

    # EUR için
p, d, q = 2, 1, 2
model_eur = ARIMA(train_data['PTF (EUR/MWh)'], order=(p, d, q))
model_fit_eur = model_eur.fit()

# Modeli kaydetme
joblib.dump(model_fit_eur, 'model_eur.pkl')


# Eğitilmiş modelleri yükleme
model_fit_tl = joblib.load('model_tl.pkl')
model_fit_usd = joblib.load('model_usd.pkl')
model_fit_eur = joblib.load('model_eur.pkl')

