import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pymongo import MongoClient


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

# Veri temizliği ve ön işleme
df['PTF (TL/MWh)'] = df['PTF (TL/MWh)'].str.replace('.', '').str.replace(',', '.').astype(float)
df['PTF (USD/MWh)'] = df['PTF (USD/MWh)'].str.replace('.', '').str.replace(',', '.').astype(float)
df['PTF (EUR/MWh)'] = df['PTF (EUR/MWh)'].str.replace('.', '').str.replace(',', '.').astype(float)

df['PTF (TL/MWh)'][df['PTF (TL/MWh)'] == 0.00] = None
df['PTF (USD/MWh)'][df['PTF (USD/MWh)'] == 0.00] = None
df['PTF (EUR/MWh)'][df['PTF (EUR/MWh)'] == 0.00] = None



# Eğitim ve test verilerini ayırma
train_ratio = 0.9
train_size = int(train_ratio * len(df))
train_data = df[:train_size]
test_data = df[train_size:]

# ARIMA modelini eğitme
# TL için
p, d, q = 4, 1, 3
model_tl = ARIMA(train_data['PTF (TL/MWh)'], order=(p, d, q))
model_fit_tl = model_tl.fit()
# USD için
p, d, q = 4, 1, 3 
model_usd = ARIMA(train_data['PTF (USD/MWh)'], order=(p, d, q))
model_fit_usd = model_usd.fit()
# EUR için
p, d, q = 5, 1, 4
model_eur = ARIMA(train_data['PTF (EUR/MWh)'], order=(p, d, q))
model_fit_eur = model_eur.fit()

# Son test verisinin saati üzerine 1 saat ekleyerek ve günü bir sonraki güne taşıyarak tahmin yapma
forecast_tl = model_fit_tl.forecast(steps=24)
forecast_usd = model_fit_usd.forecast(steps=24)
forecast_eur = model_fit_eur.forecast(steps=24)

forecast_df = pd.DataFrame({'Tarih-Saat': [],
                            'Tahmin TL': [],
                            'Tahmin USD': [],
                            'Tahmin EUR': []})

for i, (tahmin_tl, tahmin_usd, tahmin_eur) in enumerate(zip(forecast_tl, forecast_usd, forecast_eur)):
    saat = test_data.index[0] + pd.DateOffset(hours=i)
    forecast_df = forecast_df.append({'Tarih-Saat': saat,
                                      'Tahmin TL': tahmin_tl,
                                      'Tahmin USD': tahmin_usd,
                                      'Tahmin EUR': tahmin_eur}, ignore_index=True)

print(forecast_df)

