# Assuming you have your dataset
from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd

# Simulated dataset
data = {
    "Age": [31, 45, 60, 25, 35, 40, 50, 22, 28, 33, 48, 55, 19, 42, 39, 29, 47, 36, 52, 44],
    "Weight": [75, 85, 90, 60, 70, 95, 88, 55, 65, 78, 80, 92, 52, 85, 77, 68, 82, 73, 88, 79],
    "Height": [175, 165, 160, 170, 180, 165, 175, 160, 170, 175, 168, 162, 158, 172, 174, 165, 170, 167, 165, 172],
    "Heartbeat": [72, 78, 65, 80, 68, 75, 70, 85, 82, 76, 67, 73, 90, 72, 74, 83, 69, 76, 70, 72],
    "Pressure": [120, 130, 140, 115, 110, 125, 135, 120, 118, 122, 130, 138, 110, 125, 120, 115, 128, 122, 135, 125],
    "BodyTemp": [36.8, 37.0, 37.2, 36.5, 36.9, 37.1, 36.7, 36.4, 36.6, 37.0, 36.8, 37.1, 36.3, 37.0, 36.9, 36.5, 37.0, 36.7, 37.2, 36.8],
    "BreathTemp": [35.0, 36.0, 34.5, 34.8, 35.2, 35.6, 35.1, 34.9, 34.7, 35.3, 35.0, 35.5, 34.6, 35.4, 35.2, 34.8, 35.0, 35.1, 35.6, 35.2],
    "Dosage": [5, 6, 7, 4, 5.5, 6.5, 6.8, 3.8, 4.2, 5.2, 6.0, 6.7, 3.5, 5.8, 5.6, 4.5, 6.3, 5.4, 6.6, 5.9]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Features (X) and Target (y)
X = df[["Age", "Weight", "Height", "Heartbeat", "Pressure", "BodyTemp", "BreathTemp"]]
y = df["Dosage"]

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'trained_model.pkl')
