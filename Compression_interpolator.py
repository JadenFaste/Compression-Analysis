import pandas as pd
from scipy.interpolate import griddata
import numpy as np

# Load the dataset
file_path = 'Compressor_clean.xlsx'
df = pd.read_excel(file_path)

# Manually set the header based on the correct content
df.columns = ['Condensing_Temperature', 'Type', 36, 48, 55, 70, 87, 107, 130, 143, 156]

# Function to preprocess data for interpolation
def preprocess_data(data_type):
    data = df[df['Type'] == data_type]
    data = data.drop(columns=['Type']).reset_index(drop=True)
    data = data.replace({',': ''}, regex=True).apply(pd.to_numeric, errors='coerce')
    return data

# Preprocess data for all types
capacity_data = preprocess_data('C')
power_data = preprocess_data('P')
amps_data = preprocess_data('A')
mass_flow_data = preprocess_data('M')
eer_data = preprocess_data('E')
efficiency_data = preprocess_data('%')

# Prepare data for 2D interpolation
condensing_temps = capacity_data['Condensing_Temperature'].values
evap_temps = capacity_data.columns[1:].astype(float)

def prepare_points_values(data):
    values = data.iloc[:, 1:].values.flatten()
    points = np.array([(et, ct) for ct in condensing_temps for et in evap_temps])
    return points, values

capacity_points, capacity_values = prepare_points_values(capacity_data)
power_points, power_values = prepare_points_values(power_data)
amps_points, amps_values = prepare_points_values(amps_data)
mass_flow_points, mass_flow_values = prepare_points_values(mass_flow_data)
eer_points, eer_values = prepare_points_values(eer_data)
efficiency_points, efficiency_values = prepare_points_values(efficiency_data)

def interpolate_value(evap_temp, cond_temp, points, values):
    # Perform 2D interpolation
    interpolated_value = griddata(points, values, (evap_temp, cond_temp), method='linear')
    return interpolated_value

######################################################

evap_temp_input = float(input("Enter the evaporating temperature: "))
cond_temp_input = float(input("Enter the condensing temperature: "))

interpolated_capacity = interpolate_value(evap_temp_input, cond_temp_input, capacity_points, capacity_values)
interpolated_power = interpolate_value(evap_temp_input, cond_temp_input, power_points, power_values)
interpolated_amps = interpolate_value(evap_temp_input, cond_temp_input, amps_points, amps_values)
interpolated_mass_flow = interpolate_value(evap_temp_input, cond_temp_input, mass_flow_points, mass_flow_values)
interpolated_eer = interpolate_value(evap_temp_input, cond_temp_input, eer_points, eer_values)
interpolated_efficiency = interpolate_value(evap_temp_input, cond_temp_input, efficiency_points, efficiency_values)

print(f"Interpolated Capacity: {interpolated_capacity}")
print(f"Interpolated Power: {interpolated_power}")
print(f"Interpolated Amps: {interpolated_amps}")
print(f"Interpolated Mass Flow: {interpolated_mass_flow}")
print(f"Interpolated EER: {interpolated_eer}")
print(f"Interpolated Efficiency: {interpolated_efficiency}")
