import serial
import time
import requests

# Serial port setup
serial_port = 'COM11'  # Change to the correct serial port
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# ThingSpeak setup
THING_SPEAK_WRITE_API_KEY = '6NFLM8UACQUHV5JJ'  # Replace with your ThingSpeak Write API key
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Function to send data to ThingSpeak
def send_to_thingspeak(co2, heart_rate, spo2, rr):
    payload = {
        'api_key': THING_SPEAK_WRITE_API_KEY,
        'field1': co2,
        'field2': heart_rate,
        'field3': rr,
        'field4': spo2
    }
    
    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully")
        else:
            print(f"Failed to send data. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {e}")

# Read and send data every second
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        try:
            # Parse the received data
            data = line.split(",")
            timestamp = int(data[0])
            rr = int(data[1])
            co2 = float(data[2])
            hr = float(data[3])
            spo2 = float(data[4])

            # Print the received data
            print(f"Timestamp: {timestamp}, RR: {rr}, CO2: {co2}, HR: {hr}, SpO2: {spo2}")

            # Send data to ThingSpeak
            send_to_thingspeak(co2, hr, spo2, rr)

            # Wait for a while before sending the next data
            time.sleep(1)  # ThingSpeak updates once every 15 seconds, adjust accordingly

        except Exception as e:
            print(f"Error reading data: {e}")
    else:
        print("Waiting for data...")
        time.sleep(1)  # Wait for a second before checking again
