import os
import csv
import threading
import time
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PatientDetailsForm
from .models import PatientRecord
import requests
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from sklearn.preprocessing import MinMaxScaler
import os
import numpy as np
import tensorflow as tf
import pandas as pd
import requests
from django.conf import settings
from django.http import JsonResponse
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from tensorflow.keras.models import load_model
import joblib
import pickle
scaler_X = MinMaxScaler(feature_range=(0, 1))  # Adjust feature_range if needed
scaler_Y = MinMaxScaler(feature_range=(0, 1))
THINGSPEAK_CHANNEL_ID = "2860324"
THINGSPEAK_READ_API_KEY = "J3M7LJ63MIWDQB6D"
THINGSPEAK_URL = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_READ_API_KEY}&results=10"

predictions={}
model_rf = joblib.load("G:/mini project/multiclass_classifier.pkl")
model_rnn = load_model("G:/mini project/best_rnn_model.keras")
# Home view (only accessible if logged in)
@login_required
def home(request):
    if request.method == "POST":
        form = PatientDetailsForm(request.POST)
        if form.is_valid():
            # Create a new PatientRecord instance
            patient_record = PatientRecord(
                name=form.cleaned_data["name"],
                age=form.cleaned_data["age"],
            )
            patient_record.save()
            request.session["patient_id"] = patient_record.id  # Store patient ID in session
            return redirect("start_monitoring")
    else:
        form = PatientDetailsForm()
    return render(request, "home.html", {"form": form})

def predict_alarms(hr, spo2, etco2, awrr):
    # Prepare input for RF model
    input_data = np.array([[hr, spo2, etco2, awrr]])
    
    # Predict alarms
    alarms = model_rf.predict(input_data)
    return alarms[0]

def prepare_rnn_input(hr_values, spo2_values, etco2_values, awrr_values, alarms):
    # Create an array of alarms for each time step
    alarm_array = np.tile(alarms, (len(hr_values), 1))
    
    # Combine sensor data and alarms
    combined_data = np.column_stack((hr_values, spo2_values, etco2_values, awrr_values, alarm_array))
    
    # Reshape for RNN input (n_samples, time_steps, n_features)
    rnn_input = combined_data.reshape(1, combined_data.shape[0], combined_data.shape[1])
    return rnn_input

def predict_rnn(rnn_input):
    """
    Use the RNN model to predict the output for the given input.

    :param rnn_input: The preprocessed input for the RNN model.
    :return: RNN model predictions (e.g., inSEV, inO2).
    """
    # Predict with the RNN model
    predictions = model_rnn.predict(rnn_input)
    
    # Assuming the model outputs two predictions: 'inSEV' and 'inO2'
    in_sev = predictions[0][0]  # Adjust index if needed based on model output
    in_o2 = predictions[0][1]   # Adjust index if needed based on model output
    
    return in_sev, in_o2



@login_required
def start_monitoring(request):
    patient_id = request.session.get("patient_id")
    if not patient_id:
        return redirect("home")  # Ensure patient details are set

    if "start_time" not in request.session:
        request.session["start_time"] = timezone.now().isoformat()

    # Fetch the latest data from ThingSpeak
    response = requests.get(THINGSPEAK_URL)
    if response.status_code != 200:
        print("ThingSpeak request failed!")
        return render(request, "monitoring.html", {"error": "Failed to fetch data from ThingSpeak"})

    data = response.json()
    print("ThingSpeak Data:", data)  # Debugging

    if "feeds" not in data or not data["feeds"]:
        print("No feeds found!")
        return render(request, "monitoring.html", {"error": "No data available"})

    latest_feed = data["feeds"][-1]  # Get the most recent entry

    try:
        # Extract sensor data
        co2 = float(latest_feed.get("field1", 0) or 0)
        heart_rate = float(latest_feed.get("field2", 0) or 0)
        respiration_rate = float(latest_feed.get("field3", 0) or 0)
        spo2 = float(latest_feed.get("field4", 0) or 0)

        print(f"Fetched Data: CO2={co2}, HR={heart_rate}, Resp={respiration_rate}, SPO2={spo2}")  # Debugging

        # Collect recent 20 values (or less if not available)
        hr_values = [heart_rate]  # Example: replace with history from your system
        spo2_values = [spo2]
        etco2_values = [co2]
        awrr_values = [respiration_rate]

        # Ensure you have the last 20 values for each sensor, if available
        # Use actual logic for fetching and storing historical data

        # Predict alarms with RF model (using the most recent data)
        alarms = predict_alarms(hr_values[-1], spo2_values[-1], etco2_values[-1], awrr_values[-1])

        # Prepare RNN input (for the last 20 readings, including the alarms)
        rnn_input = prepare_rnn_input(hr_values[-20:], spo2_values[-20:], etco2_values[-20:], awrr_values[-20:], alarms)

        # Predict with RNN model
        rnn_predictions = predict_rnn(rnn_input)

        # Rescale or process RNN predictions if needed
        # In this example, rnn_predictions might contain 'inSEV' and 'inO2' (as per your initial code)
        in_sev, in_o2 = rnn_predictions

        predictions = {
            "co2": co2,
            "heart_rate": heart_rate,
            "respiration_rate": respiration_rate,
            "spo2": spo2,
            "alarms": alarms,
            "rnn_predictions": {"inSEV": in_sev, "inO2": in_o2}
        }

        print("Predictions:", predictions)  # Debugging

    except Exception as e:
        print("Error in prediction:", str(e))  # Debugging
        return render(request, "monitoring.html", {"error": str(e)})

    return render(request, "monitoring.html", {"predictions": predictions})

# Fetch data from ThingSpeak and save to database
@login_required
def fetch_data(request):
    # Get the start time from session
    start_time = request.session.get("start_time")
    if not start_time:
        return JsonResponse({"error": "Start time not set"}, status=400)

    # Convert start_time from string to datetime
    start_time = parse_datetime(start_time)

    # Make the API request to ThingSpeak
    response = requests.get(THINGSPEAK_URL)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch data from ThingSpeak"}, status=500)
    
    data = response.json()

    # Parse data from the cloud (e.g., ThingSpeak)
    timestamps = []
    co2_values = []
    heart_rate_values = []
    respiration_rate_values = []
    spo2_values = []

    # Filter data based on the start_time
    for feed in data.get("feeds", []):
        feed_time = parse_datetime(feed["created_at"])
        if feed_time >= start_time:
            timestamps.append(feed["created_at"])
            co2_values.append(float(feed.get("field1", 0)))
            heart_rate_values.append(float(feed.get("field2") or 0))
            respiration_rate_values.append(float(feed.get("field3") or 0))
            spo2_values.append(float(feed.get("field4") or 0))

    return JsonResponse({
        "timestamps": timestamps,
        "co2_values": co2_values,
        "heart_rate_values": heart_rate_values,
        "respiration_rate_values": respiration_rate_values,
        "spo2_values": spo2_values
    })

# Stop monitoring and finalize the record
@login_required
def stop_monitoring(request):
    patient_id = request.session.get("patient_id")
    if not patient_id:
        return JsonResponse({"error": "Patient ID not found"}, status=400)

    # Clear the patient id and start time from session
    request.session.pop("patient_id", None)
    request.session.pop("start_time", None)

    return JsonResponse({"success": True, "message": "Monitoring stopped and data saved."})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("login_success")  # Redirect to home after login
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")

# Database view to show all patient records
@login_required
def patient_database(request):
    records = PatientRecord.objects.all()
    return render(request, "patient_database.html", {"records": records})

# Index view
def index(request):
    return render(request, "index.html")

@login_required
def login_success(request):
    # Render the login success page
    return render(request, "login_success.html")



# View to start surgery (start continuous fetching)
predictions = {}  # Initialize empty dict for predictions
surgery_active = False

@csrf_exempt
@login_required
def start_surgery(request):
    global surgery_active, predictions
    
    # Set the flag to True to keep the thread running
    surgery_active = True
    
    def fetch_and_predict():
        global surgery_active, predictions
        
        print("Background thread started!")  # Debug message
        
        while surgery_active:
            try:
                # Fetch data from ThingSpeak
                response = requests.get(THINGSPEAK_URL)
                if response.status_code == 200:
                    data = response.json()
                    if "feeds" in data and data["feeds"]:
                        latest_feed = data["feeds"][-1]
                        
                        # Extract sensor data
                        co2 = float(latest_feed.get("field1", 0) or 0)
                        heart_rate = float(latest_feed.get("field2", 0) or 0)
                        respiration_rate = float(latest_feed.get("field3", 0) or 0)
                        spo2 = float(latest_feed.get("field4", 0) or 0)
                        
                        print(f"Fetched Data: CO2={co2}, HR={heart_rate}, Resp={respiration_rate}, SPO2={spo2}")

                        # Predict alarms with RF model
                        alarms = predict_alarms(heart_rate, spo2, co2, respiration_rate)
                        
                        # Prepare RNN input (using single values for simplicity)
                        hr_values = [heart_rate]
                        spo2_values = [spo2]
                        etco2_values = [co2]
                        awrr_values = [respiration_rate]
                        
                        # Prepare RNN input
                        rnn_input = prepare_rnn_input(hr_values, spo2_values, etco2_values, awrr_values, alarms)
                        
                        # Predict with RNN model
                        in_sev, in_o2 = predict_rnn(rnn_input)
                        
                        # Update global predictions variable
                        predictions = {
                            "co2": co2,
                            "heart_rate": heart_rate,
                            "respiration_rate": respiration_rate,
                            "spo2": spo2,
                            "alarms": alarms.tolist() if hasattr(alarms, 'tolist') else alarms,
                            "rnn_predictions": {"inSEV": float(in_sev), "inO2": float(in_o2)}
                        }
                        
                        print("Updated predictions:", predictions)
                
            except Exception as e:
                print(f"Error in fetch_and_predict thread: {str(e)}")
            
            # Sleep for a few seconds before next update
            time.sleep(5)
    
    # Start a background thread to fetch and predict continuously
    thread = threading.Thread(target=fetch_and_predict, daemon=True)
    thread.start()
    
    return JsonResponse({"status": "Surgery started, data fetching in progress..."})

@csrf_exempt
@login_required
def stop_surgery(request):
    # Add logic to stop the continuous fetching here
    # For now, we can just return a response indicating surgery stopped
    return JsonResponse({"status": "Surgery stopped"})

@login_required
def predict_data(request):
    # Fetch the most recent predictions (this can be stored in a variable, DB, or cache)
    predictions = {
        "co2": 0.5,
        "heart_rate": 75,
        "respiration_rate": 16,
        "spo2": 98,
        "alarms": "None",
        "rnn_predictions": {
            "inSEV": 0.85,
            "inO2": 0.92
        }
    }
    return JsonResponse(predictions)

surgery_active = False

# New view to get the latest predictions
@login_required
def get_latest_predictions(request):
    
    # Log the data being sent
    print("Sending to template:", predictions)
    
    # Return an empty dict if latest_predictions is not initialized
    if not predictions:
        return JsonResponse({
            "status": "waiting",
            "message": "No predictions available yet"
        })
    
    # Return the latest predictions
    return JsonResponse(predictions)