import numpy as np
import tensorflow as tf

# Load your trained RNN model
model = tf.keras.models.load_model('best_rnn_model (1).keras')  # Replace with your actual model file

# Generate or load test input data
# Example: Creating a random test sample (modify based on your actual input shape)
test_input = np.array([[70, 98, 40, 16]])  # Replace with actual HR, SpO2, etCO2, awRR values
test_input = test_input.reshape(1, 1, 4)  # Reshape as (batch_size, timesteps, features)

# Get the model's prediction
predicted_dosage = model.predict(test_input)

# Display the result
print(f"Predicted anesthesia dosage: {predicted_dosage[0][0]:.2f} mL")
