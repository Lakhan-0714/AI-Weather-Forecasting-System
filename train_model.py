import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv("weather.csv")

# Show first 5 rows
print(data.head())

# Features (inputs)
X = data[['Humidity', 'Pressure', 'Wind_Speed']]

# Target (output)
y = data['Temperature']

# Create the model
model = RandomForestRegressor()

# Train the model
model.fit(X, y)

print("Model trained successfully!")

# Save the trained model
joblib.dump(model, "weather_model.pkl")

print("Model saved successfully!")