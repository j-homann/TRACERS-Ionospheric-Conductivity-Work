# Imports
import spaceToolsLib as stl
import numpy as np
from scipy.integrate import simpson
import tqdm

# Loading the data file
file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\l3\ts2_l3_ace_pitch-angle-dist-pre_20251231_v0.2.0.cdf"
data_dict = stl.loadDictFromFile(file)

# Getting the data and converting pitch angle from degrees to radians
differential_energy_flux = data_dict['ts2_l3_ace_pitch_def'][0]
Energy = data_dict['ts2_l3_ace_energy'][0]
pitch_angle = (np.pi/180) * data_dict['ts2_l3_ace_pitch_angle'][0]
Epoch = data_dict['Epoch'][0]

# Ensure there are no negative values in differential_energy_flux
differential_energy_flux = np.clip(differential_energy_flux, 0.01, None)

# Sorting Energy into ascending order to avoid a negative energy_flux
Energy.sort()

# Calculating energy flux
flux_integrand = differential_energy_flux * np.sin(pitch_angle)
I_pitch = simpson(flux_integrand, pitch_angle, axis=2) * (2 * np.pi)
energy_flux = simpson(I_pitch, Energy, axis=1)

# Reshaping Energy so Energy * differential_energy_flux can be calculated without an error
Energy_reshaped = Energy[np.newaxis, :, np.newaxis]

# Calculating characteristic energy
characteristic_energy_integrand = Energy_reshaped * differential_energy_flux * np.sin(pitch_angle)
I_pitch = simpson(characteristic_energy_integrand, pitch_angle, axis=2) * (2 * np.pi)
characteristic_energy_flux = simpson(I_pitch, Energy, axis=1)
characteristic_energy = characteristic_energy_flux/energy_flux
print(characteristic_energy_flux)

# Calculating Pedersen and Hall conductances according to (Robinson et al., 1987)
pedersen_conductance = (40 * characteristic_energy / (16 + characteristic_energy**2)) * energy_flux**(1/2)
hall_conductance = 0.45 * characteristic_energy**(0.85) * pedersen_conductance

# Creating a dictionary for the CDF file
data_dict_output = {
    'energy_flux': [np.array(energy_flux), {'UNITS': 'eV/cm^2-s', 'DEPEND_0': 'Epoch', 'LABLAXIS': 'Energy Flux'}],
    'characteristic_energy': [np.array(characteristic_energy), {'UNITS': 'ev^2/cm^2-s', 'DEPEND_0': 'Epoch', 'LABLAXIS': 'Characteristic Energy'}],
    'pedersen_conductance': [np.array(pedersen_conductance), {'UNITS': 'S', 'DEPEND_0': 'Epoch', 'LABLAXIS': 'Pedersen Conductance'}],
    'hall_conductance': [np.array(hall_conductance), {'UNITS': 'S', 'DEPEND_0': 'Epoch', 'LABLAXIS': 'Hall Conductance'}],
    'Epoch': [np.array(Epoch), {'UNITS': 's', 'LABLAXIS': 'Epoch'}]
    }

# Outputting the results to the file
output_file = "C:/Users/jason/OneDrive/Documents/TRACERS/Science/Omni_Directional_Flux.cdf"
stl.outputCDFdata(output_file, data_dict_output)