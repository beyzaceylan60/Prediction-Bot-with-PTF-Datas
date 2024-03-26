# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:32:29 2024

@author: sarid
"""

import pandas as pd
import os
import joblib

model_fit_tl = joblib.load('model_tl.pkl')
model_fit_usd = joblib.load('model_usd.pkl')
model_fit_eur = joblib.load('model_eur.pkl')

forecast_tl = model_fit_tl.forecast(steps=24)
forecast_usd = model_fit_usd.forecast(steps=24)
forecast_eur = model_fit_eur.forecast(steps=24)

forecast_df = pd.DataFrame({
                            'Tahmin TL': [],
                            'Tahmin USD': [],
                            'Tahmin EUR': []})

for i, (tahmin_tl, tahmin_usd, tahmin_eur) in enumerate(zip(forecast_tl, forecast_usd, forecast_eur)):
    forecast_df = forecast_df.append({
                                      'Tahmin TL': tahmin_tl,
                                      'Tahmin USD': tahmin_usd,
                                      'Tahmin EUR': tahmin_eur}, ignore_index=True)
html_content = forecast_df.to_html()
with open('Veritabani_Projesi.html', 'w') as f:
    f.write(html_content)
path = os.path.join(os.getcwd(), "Veritabani_Projesi.html")
os.startfile(path)      
print(forecast_df)
