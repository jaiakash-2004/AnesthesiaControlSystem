import requests
import time

# ThingSpeak API details
THINGSPEAK_WRITE_API_KEY = "6NFLM8UACQUHV5JJ"  # Replace with your ThingSpeak API key
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def send_to_thingspeak(dosage, heart_rate, oxygen_level, blood_pressure):
    """Send anesthesia dosage and patient vitals to ThingSpeak."""
    
    payload = {
        "api_key": THINGSPEAK_WRITE_API_KEY,
        "field1": dosage,         # Predicted anesthesia dosage (mL)
        "field2": heart_rate,     # Heart rate (BPM)
        "field3": oxygen_level,   # Oxygen saturation (SpO2)
        "field4": blood_pressure  # Blood pressure (mmHg)
    }

    response = requests.get(THINGSPEAK_URL, params=payload)

    if response.status_code == 200:
        print(f"Data sent: Dosage={dosage}mL, HR={heart_rate}BPM, SpO2={oxygen_level}%, BP={blood_pressure}mmHg")
    else:
        print(f"Failed to send data. Error: {response.status_code}")

# Example: Sending data every 15 seconds
while True:
    predicted_dosage = 3.5   # Example: ML model predicted 3.5 mL of anesthesia
    heart_rate = 75          # Example: 75 BPM
    oxygen_level = 98        # Example: 98% SpO2
    blood_pressure = 120     # Example: 120 mmHg

    send_to_thingspeak(predicted_dosage, heart_rate, oxygen_level, blood_pressure)
    
    time.sleep(1)  # Send data every 15 seconds
