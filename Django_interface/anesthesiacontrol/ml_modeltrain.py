import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import layers, models

# Load the dataset
data = pd.read_csv('patient_data.csv')

# Separate features and target variable (dosage)
X = data[['patient_id', 'age', 'height', 'weight', 'heart_rate', 'body_temp', 'breath_temp']]
y = data['dosages']

# Preprocessing the data
# Standardizing the features (mean=0, std=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape X_scaled to 3D array for RNN input
X_scaled = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])  # 3D shape: (samples, timesteps, features)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the RNN model
model = models.Sequential([
    layers.SimpleRNN(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)  # Output layer (dosage prediction)
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Evaluate the model on the test data
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}, Test MAE: {test_mae}')

# Make predictions
predictions = model.predict(X_test)
print(f'Predictions: {predictions}')

# Save the trained model
model.save('anesthesia_model.h5')
