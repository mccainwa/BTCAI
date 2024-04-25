import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the datasets
btc_2017 = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-2017min.csv')
btc_2018 = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-2018min.csv')
btc_2019 = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-2019min.csv')
btc_2020 = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-2020min.csv')
btc_2021 = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-2021min.csv')

# Combine all the datasets
btc_yearly = pd.concat([btc_2017, btc_2018, btc_2019, btc_2020, btc_2021])

# Ensure 'date' is in datetime format
btc_yearly['date'] = pd.to_datetime(btc_yearly['date'])

# Create lagged features based on the previous day
btc_yearly['prev_open'] = btc_yearly['open'].shift(1)
btc_yearly['prev_high'] = btc_yearly['high'].shift(1)
btc_yearly['prev_low'] = btc_yearly['low'].shift(1)
btc_yearly['prev_close'] = btc_yearly['close'].shift(1)
btc_yearly['prev_volume_btc'] = btc_yearly['Volume BTC'].shift(1)

# Drop the first row to remove NaN values from lagged features
btc_yearly_cleaned = btc_yearly.dropna()

# Define features and targets
X_yearly = btc_yearly_cleaned[['prev_open', 'prev_high', 'prev_low', 'prev_close', 'prev_volume_btc']]
y_high_yearly = btc_yearly_cleaned['high']
y_low_yearly = btc_yearly_cleaned['low']

# Split data into training and testing sets
X_train_yearly, X_test_yearly, y_high_train_yearly, y_high_test_yearly = train_test_split(X_yearly, y_high_yearly, test_size=0.2, random_state=42, shuffle=False)
X_train_yearly, X_test_yearly, y_low_train_yearly, y_low_test_yearly = train_test_split(X_yearly, y_low_yearly, test_size=0.2, random_state=42, shuffle=False)

# Train linear regression models for high and low prices
model_high_yearly = LinearRegression()
model_low_yearly = LinearRegression()

model_high_yearly.fit(X_train_yearly, y_high_train_yearly)
model_low_yearly.fit(X_train_yearly, y_low_train_yearly)

# Make predictions
y_high_pred_yearly = model_high_yearly.predict(X_test_yearly)
y_low_pred_yearly = model_low_yearly.predict(X_test_yearly)

# Evaluate the models
rmse_high_yearly = np.sqrt(mean_squared_error(y_high_test_yearly, y_high_pred_yearly))
r2_high_yearly = r2_score(y_high_test_yearly, y_high_pred_yearly)

rmse_low_yearly = np.sqrt(mean_squared_error(y_low_test_yearly, y_low_pred_yearly))
r2_low_yearly = r2_score(y_low_test_yearly, y_low_pred_yearly)

print("Yearly High Price Prediction - RMSE:", rmse_high_yearly, "R²:", r2_high_yearly)
print("Yearly Low Price Prediction - RMSE:", rmse_low_yearly, "R²:", r2_low_yearly)

# Visualization
plt.figure(figsize=(14, 7))

# High Prices
plt.subplot(1, 2, 1)
plt.plot(btc_yearly_cleaned['date'][-len(y_high_test_yearly):], y_high_test_yearly, label='Actual High Prices', color='blue', marker='.')
plt.plot(btc_yearly_cleaned['date'][-len(y_high_pred_yearly):], y_high_pred_yearly, label='Predicted High Prices', color='red', linestyle='--')
plt.title('Yearly Actual vs Predicted High Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

# Low Prices
plt.subplot(1, 2, 2)
plt.plot(btc_yearly_cleaned['date'][-len(y_low_test_yearly):], y_low_test_yearly, label='Actual Low Prices', color='green', marker='.')
plt.plot(btc_yearly_cleaned['date'][-len(y_low_pred_yearly):], y_low_pred_yearly, label='Predicted Low Prices', color='orange', linestyle='--')
plt.title('Yearly Actual vs Predicted Low Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
