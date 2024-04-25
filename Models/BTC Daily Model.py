import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the daily Bitcoin data
btc_daily = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-Daily.csv')

# Convert 'date' column to datetime format (if it's not already)
btc_daily['date'] = pd.to_datetime(btc_daily['date'])

# Feature Engineering: Create lagged features for the previous day's prices and volume
btc_daily['prev_open'] = btc_daily['open'].shift(1)
btc_daily['prev_high'] = btc_daily['high'].shift(1)
btc_daily['prev_low'] = btc_daily['low'].shift(1)
btc_daily['prev_close'] = btc_daily['close'].shift(1)
btc_daily['prev_volume_btc'] = btc_daily['Volume BTC'].shift(1)

# Drop the first row since it will have NaN values for the lagged features
btc_daily_cleaned = btc_daily.dropna()

# Selecting features and targets
X = btc_daily_cleaned[['prev_open', 'prev_high', 'prev_low', 'prev_close', 'prev_volume_btc']]
y_high = btc_daily_cleaned['high']
y_low = btc_daily_cleaned['low']

# Splitting the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_high_train, y_high_test = train_test_split(X, y_high, test_size=0.2, random_state=42, shuffle=False)
X_train, X_test, y_low_train, y_low_test = train_test_split(X, y_low, test_size=0.2, random_state=42, shuffle=False)

# Initialize and train the linear regression models
model_high = LinearRegression()
model_low = LinearRegression()

model_high.fit(X_train, y_high_train)
model_low.fit(X_train, y_low_train)

# Predict on the test set
y_high_pred = model_high.predict(X_test)
y_low_pred = model_low.predict(X_test)

# Evaluate the models
rmse_high = np.sqrt(mean_squared_error(y_high_test, y_high_pred))
r2_high = r2_score(y_high_test, y_high_pred)

rmse_low = np.sqrt(mean_squared_error(y_low_test, y_low_pred))
r2_low = r2_score(y_low_test, y_low_pred)

print("High Price Prediction Model: RMSE =", rmse_high, ", R² =", r2_high)
print("Low Price Prediction Model: RMSE =", rmse_low, ", R² =", r2_low)

# Actual vs. Predicted High Prices
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)  # This means 1 row, 2 columns, and this plot is the 1st plot.
plt.plot(btc_daily_cleaned['date'][-len(y_high_test):], y_high_test, label='Actual High Prices', color='blue', marker='.')
plt.plot(btc_daily_cleaned['date'][-len(y_high_pred):], y_high_pred, label='Predicted High Prices', color='red', linestyle='--')
plt.title('Actual vs Predicted High Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

# Actual vs. Predicted Low Prices
plt.subplot(1, 2, 2)  # This means 1 row, 2 columns, and this plot is the 2nd plot.
plt.plot(btc_daily_cleaned['date'][-len(y_low_test):], y_low_test, label='Actual Low Prices', color='green', marker='.')
plt.plot(btc_daily_cleaned['date'][-len(y_low_pred):], y_low_pred, label='Predicted Low Prices', color='orange', linestyle='--')
plt.title('Actual vs Predicted Low Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()