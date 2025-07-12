# Anesthesia Control System using Machine Learning and IoT

This project is an **automated anesthesia dosage recommendation and monitoring system** using **Machine Learning (ML)** models and **IoT-based real-time vitals monitoring**. The system is designed to assist anesthesiologists by providing intelligent dosage suggestions based on patient vitals.

---

## 🔧 Features

- 🧠 **RNN-based dosage prediction**
- 🌡️ Real-time vitals data collection (SpO₂, heart rate, respiration, CO₂ levels)
- 📊 Cloud integration for monitoring using **ThingSpeak**
- 📦 Django-based web interface for data logging and analysis
- 🧪 Trained ML models with >85% accuracy on synthetic & patient data

---

## 🧪 Technologies Used

- **Python, Django**
- **Recurrent Neural Networks (RNN)**
- **ESP32**, MAX30100, CO₂ sensor, Thermistor
- **ThingSpeak** for IoT cloud
- **Pandas, NumPy, scikit-learn, Keras, TensorFlow**
- **HTML/CSS** (for web frontend)

---

## 📁 Project Structure

```bash
├── Django_interface/       # Web interface & backend
├── ML model/               # Notebooks, training scripts, model files
├── Outputs/                # Visualizations and results
├── csv_files/              # Case-wise vitals data
├── *.pkl / *.keras         # Saved ML models
├── test.py                 # Script for testing model
