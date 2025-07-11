import pandas as pd

# Load the dataset
file_path = 'uq_vsd_case01_trenddata.csv'  # Adjust path as needed
data = pd.read_csv(file_path)

# Display initial columns to understand the structure
print("Initial Columns:", data.columns)

# Select relevant columns for anesthetic concentrations and tidal volume
anesthetic_columns = ['etDES', 'etISO', 'etSEV', 'etN2O']  # Adjust based on your dataset's actual column names
tidal_volume_column = 'Tidal Volume'  # Ensure this matches your dataset's tidal volume column name

# Create a new DataFrame to store dosages
dosage_data = pd.DataFrame()

# Calculate dosages based on concentrations and tidal volume
for column in anesthetic_columns:
    if column in data.columns:
        # Assuming concentration is in percentage (%)
        dosage_data[column + '_Dosage_mL'] = data[column] * (data[tidal_volume_column] / 100)  # Convert % to mL

# Combine with original data if needed
result_data = pd.concat([data, dosage_data], axis=1)

# Display results
print(result_data[[tidal_volume_column, *anesthetic_columns, *dosage_data.columns]].head())

# Optionally save to a new CSV file
result_data.to_csv('anesthesia_dosage_calculations_mL.csv', index=False)
