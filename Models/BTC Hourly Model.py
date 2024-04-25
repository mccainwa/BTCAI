import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the hourly Bitcoin data
btc_hourly = pd.read_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/BTC Data/BTC-Hourly.csv')

# Ensure 'date' is in datetime format
btc_hourly['date'] = pd.to_datetime(btc_hourly['date'])

# Create lagged features based on the previous hour
btc_hourly['prev_open'] = btc_hourly['open'].shift(1)
btc_hourly['prev_high'] = btc_hourly['high'].shift(1)
btc_hourly['prev_low'] = btc_hourly['low'].shift(1)
btc_hourly['prev_close'] = btc_hourly['close'].shift(1)
btc_hourly['prev_volume_btc'] = btc_hourly['Volume BTC'].shift(1)

# Drop the first row to remove NaN values from lagged features
btc_hourly_cleaned = btc_hourly.dropna()

# Define features and targets
X_hourly = btc_hourly_cleaned[['prev_open', 'prev_high', 'prev_low', 'prev_close', 'prev_volume_btc']]
y_high_hourly = btc_hourly_cleaned['high']
y_low_hourly = btc_hourly_cleaned['low']

# Split data into training and testing sets
X_train_hourly, X_test_hourly, y_high_train_hourly, y_high_test_hourly = train_test_split(X_hourly, y_high_hourly, test_size=0.2, random_state=42, shuffle=False)
X_train_hourly, X_test_hourly, y_low_train_hourly, y_low_test_hourly = train_test_split(X_hourly, y_low_hourly, test_size=0.2, random_state=42, shuffle=False)

# Train linear regression models for high and low prices
model_high_hourly = LinearRegression()
model_low_hourly = LinearRegression()

model_high_hourly.fit(X_train_hourly, y_high_train_hourly)
model_low_hourly.fit(X_train_hourly, y_low_train_hourly)

# Make predictions
y_high_pred_hourly = model_high_hourly.predict(X_test_hourly)
y_low_pred_hourly = model_low_hourly.predict(X_test_hourly)

# Evaluate the models
rmse_high = np.sqrt(mean_squared_error(y_high_test_hourly, y_high_pred_hourly))
r2_high = r2_score(y_high_test_hourly, y_high_pred_hourly)

rmse_low = np.sqrt(mean_squared_error(y_low_test_hourly, y_low_pred_hourly))
r2_low = r2_score(y_low_test_hourly, y_low_pred_hourly)

print("High Price Prediction - RMSE:", rmse_high, "R²:", r2_high)
print("Low Price Prediction - RMSE:", rmse_low, "R²:", r2_low)

# Save predictions to CSV
predictions = pd.DataFrame({
    'date': btc_hourly_cleaned['date'][-len(y_high_pred_hourly):],
    'actual_high': y_high_test_hourly,
    'predicted_high': y_high_pred_hourly,
    'actual_low': y_low_test_hourly,
    'predicted_low': y_low_pred_hourly
})
predictions.to_csv('C:/Users/param/OneDrive - Loyola University Chicago/Comp 379/predictions_hourly.csv', index=False)

# Visualization
plt.figure(figsize=(14, 7))

# High Prices
plt.subplot(1, 2, 1)
plt.plot(predictions['date'], predictions['actual_high'], label='Actual High Prices', color='blue', marker='.')
plt.plot(predictions['date'], predictions['predicted_high'], label='Predicted High Prices', color='red', linestyle='--')
plt.title('Hourly Actual vs Predicted High Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

# Low Prices
plt.subplot(1, 2, 2)
plt.plot(predictions['date'], predictions['actual_low'], label='Actual Low Prices', color='green', marker='.')
plt.plot(predictions['date'], predictions['predicted_low'], label='Predicted Low Prices', color='orange', linestyle='--')
plt.title('Hourly Actual vs Predicted Low Prices')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
