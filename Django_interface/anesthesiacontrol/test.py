import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Load the RNN model
rnn_model = load_model("best_rnn_model.keras")  # Path to your saved RNN model

# Define MinMaxScaler with the same feature_range as used during training
scaler_X = MinMaxScaler(feature_range=(0, 1))  # Adjust feature_range if needed
scaler_Y = MinMaxScaler(feature_range=(0, 1))  # Adjust feature_range if needed

# Generate dummy input data
# Example: 20 time steps with 4 features (HR, SpO2, etCO2, awRR)
dummy_data = np.array([
    [72, 98, 35, 16],  # Time step 1
    [73, 97, 36, 15],  # Time step 2
    [74, 96, 37, 14],  # Time step 3
    [75, 95, 38, 13],  # Time step 4
    [76, 94, 39, 12],  # Time step 5
    [77, 93, 40, 11],  # Time step 6
    [78, 92, 41, 10],  # Time step 7
    [79, 91, 42, 9],   # Time step 8
    [80, 90, 43, 8],   # Time step 9
    [81, 89, 44, 7],   # Time step 10
    [82, 88, 45, 6],   # Time step 11
    [83, 87, 46, 5],   # Time step 12
    [84, 86, 47, 4],   # Time step 13
    [85, 85, 48, 3],   # Time step 14
    [86, 84, 49, 2],   # Time step 15
    [87, 83, 50, 1],   # Time step 16
    [88, 82, 51, 0],   # Time step 17
    [89, 81, 52, 1],   # Time step 18
    [90, 80, 53, 2],   # Time step 19
    [91, 79, 54, 3],   # Time step 20
])

# Fit the scaler on the dummy data (for demonstration purposes)
# In practice, you should use the same scaler that was fitted on the training data.
scaler_X.fit(dummy_data)
scaler_Y.fit(np.array([[0, 0], [100, 100]]))  # Example range for targets

# Normalize the dummy data using the MinMaxScaler
dummy_data_scaled = scaler_X.transform(dummy_data)

# Reshape the dummy data for RNN input: (1, time_steps, features)
# Here, time_steps = 20, features = 4
dummy_data_reshaped = dummy_data_scaled[np.newaxis, :, :]

# Make predictions using the RNN model
predictions_scaled = rnn_model.predict(dummy_data_reshaped)

# Convert predictions back to the original scale
predictions = scaler_Y.inverse_transform(predictions_scaled)

# Print the results
print("Dummy Input Data (Original Scale):")
print(dummy_data)
print("\nPredictions (Original Scale):")
print(predictions)