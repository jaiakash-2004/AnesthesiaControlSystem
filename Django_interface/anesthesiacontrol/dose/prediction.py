import joblib

# Load the trained model
model = joblib.load('G:/mini project/Anesthesia control/trained_model.pkl')

def predict_dosage(age, weight, height, heartbeat, pressure, body_temp, breath_temp):
    features = [[age, weight, height, heartbeat, pressure, body_temp, breath_temp]]
    predicted_dosage = model.predict(features)
    return predicted_dosage[0]
