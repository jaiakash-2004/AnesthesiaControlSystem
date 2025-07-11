import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('training_history (1).csv')

# Plotting the data
plt.figure(figsize=(14, 6))

# Plot accuracy and validation accuracy
plt.subplot(1, 2, 1)
plt.plot(data['accuracy'], label='Training Accuracy')
plt.plot(data['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Plot loss and validation loss
plt.subplot(1, 2, 2)
plt.plot(data['loss'], label='Training Loss')
plt.plot(data['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Adjust layout
plt.tight_layout()
plt.show()