import numpy as np
import pandas as pd

def simulate_patient_data(patient_id, duration_minutes=60):
    """
    Simulates vital signs and anesthesia dosage for a single patient.

    Args:
        patient_id: ID of the patient.
        duration_minutes: Duration of the simulation in minutes.

    Returns:
        pandas DataFrame containing simulated data.
    """

    time_steps = duration_minutes * 60  # Number of data points per minute
    time = np.arange(0, duration_minutes * 60)

    # Initial values
    heartbeat = 72
    spo2 = 98
    body_temp = 36.8
    resp_rate = 14
    anesthesia_dosage = 0.2

    # Noise factors
    heartbeat_noise = np.random.normal(0, 2, time_steps) 
    spo2_noise = np.random.normal(0, 0.5, time_steps)
    body_temp_noise = np.random.normal(0, 0.1, time_steps)
    resp_rate_noise = np.random.normal(0, 1, time_steps)

    # Simulate data with basic relationships
    data = pd.DataFrame({
        'Time': time,
        'Heartbeat': np.clip(heartbeat + heartbeat_noise + 
                            0.01 * anesthesia_dosage * np.sin(time/10), 60, 120),
        'SpO2': np.clip(spo2 + spo2_noise - 
                       0.1 * anesthesia_dosage + 0.05 * resp_rate_noise, 95, 100),
        'Body Temperature': np.clip(body_temp + body_temp_noise, 36.0, 37.5),
        'Respiration Rate': np.clip(resp_rate + resp_rate_noise - 
                                  0.2 * anesthesia_dosage, 12, 20),
        'Anesthesia Dosage': np.clip(anesthesia_dosage + 
                                   0.05 * np.sin(time/20) + 
                                   0.02 * heartbeat_noise, 0.1, 0.5)
    })

    return data

# Simulate data for 20 patients
all_patient_data = []
for i in range(1, 21):
    patient_data = simulate_patient_data(i)
    patient_data['Patient'] = i
    all_patient_data.append(patient_data)

# Concatenate all patient data
simulated_dataset = pd.concat(all_patient_data)

# Save the simulated dataset
simulated_dataset.to_csv('simulated_anesthesia_data.csv', index=False)