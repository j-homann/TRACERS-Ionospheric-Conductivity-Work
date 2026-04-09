import numpy as np
from scipy.integrate import simpson
import spaceToolsLib as stl
import datetime as dt
from Functions import compute_energy_flux, compute_average_energy, restrict_angle_range, restrict_energy_range

'''Pre-defined toggles for our data'''
# What day we are examining
date = 20260115

# Electron energy limits based on (Robinson et al., 1987)
electron_energy_min = 500       # eV
electron_energy_max = 15000     # eV

# Ion energy limits based on (Galand & Richmond, 2001)
ion_energy_min = 2000       # eV
ion_energy_max = 40000      # eV

# Only counting precipitating (downward) flux
pitch_angle_min = -np.pi/2
pitch_angle_max = np.pi / 2

# Getting the magnetic field from the CHAOS model
# Latitude and Longitude of Svalbard in degrees, height in km
B_model = stl.CHAOS(np.array([77.8750]), np.array([20.9752]), np.array([110]), np.array([dt.datetime(2025, 1, 15, 10, 10)]))
B_110 = np.linalg.norm(B_model[0]) * (1e-9) # Converted to nT
B_0 = 54000e-9

'''Loading files and data'''
# Loading the data files
ace_file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\ACE\l3\ts2_l3_ace_pitch-angle-dist_{date}_v1.2.0.cdf"
aci_file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\ACI\l2\ts2_l2_aci_ipd_{date}_v1.0.2.cdf"

# Defining our data dictionary
data = {
    'ACE': stl.loadDictFromFile(ace_file),
    'ACI': stl.loadDictFromFile(aci_file)
}

'''Electron Contribution'''
# Getting ACE data
ace_def = data['ACE']['ts2_l3_ace_pitch_def'][0] # eV / eV cm^2 sr s
ace_energy = data['ACE']['ts2_l3_ace_energy'][0]
ace_pitch = np.deg2rad(data['ACE']['ts2_l3_ace_pitch_angle'][0]) # Converted from degrees to radians

# Restrict pitch angle and energy based off our defined limits
ace_pitch, ace_def = restrict_angle_range(ace_pitch, ace_def, pitch_angle_min, pitch_angle_max)
ace_energy, ace_def = restrict_energy_range(ace_energy, ace_def, electron_energy_min, electron_energy_max)

# Remove negative or zero values so errors aren't thrown in later calculations
ace_def = np.clip(ace_def, 0.01, None)

# Flip energy axis to avoid negative values in integration
ace_energy = np.flip(ace_energy)
ace_def = np.flip(ace_def, axis=1)

# Electron energy flux converted from eV / cm^2 s to ergs / cm^2 s (Or mW / m^2 in SI)
electron_energy_flux = (1.6e-19) * (1e7) * compute_energy_flux(ace_def, ace_energy, ace_pitch)

# Average energy
average_electron_energy = compute_average_energy(ace_def, ace_energy, ace_pitch, electron_energy_flux)
average_electron_energy /= 1000   # Converted from eV to keV
print(np.min(average_electron_energy))
print(np.max(average_electron_energy))

# Electron Pedersen and Hall conductances
electron_pedersen_conductance = ((40 * average_electron_energy /(16 + average_electron_energy**2))
                                 * np.sqrt(electron_energy_flux))
electron_hall_conductance = 0.45 * average_electron_energy**0.85 * electron_pedersen_conductance

'''Ion Contribution'''
# Getting ACI data
aci_def = data['ACI']['ts2_l2_aci_tscs_def'][0]
aci_energy = data['ACI']['ts2_l2_aci_energy'][0]
aci_angle = np.deg2rad(data['ACI']['ts2_l2_aci_tscs_anode_angle'][0]) # Converted from degrees to radians

# Restrict angle and energy based off our defined limits
aci_angle, aci_def = restrict_angle_range(aci_angle, aci_def, pitch_angle_min, pitch_angle_max)
aci_energy, aci_def = restrict_energy_range(aci_energy, aci_def, ion_energy_min, ion_energy_max)

# Remove negative or zero values so errors aren't thrown in later calculations
aci_def = np.clip(aci_def, 0.01, None)

# Ion energy flux converted from eV / cm^2 s to ergs / cm^2 s (Or mW / m^2 in SI)
ion_energy_flux = (1.6e-19) * (1e7) * compute_energy_flux(aci_def, aci_energy, aci_angle)

# Average ion energy
average_ion_energy = compute_average_energy(aci_def, aci_energy, aci_angle, ion_energy_flux)
average_ion_energy /= 1000   # Converted from eV to keV
print(np.min(average_ion_energy))
print(np.max(average_ion_energy))

# Ion Pedersen and Hall conductances
ion_pedersen_conductance = 5.7 * np.sqrt(ion_energy_flux) * (B_110/B_0)**-1.45
ion_hall_conductance = 2.6 * average_ion_energy**0.3 * np.sqrt(ion_energy_flux) * (B_110/B_0)**-1.90

'''Solar EUV Contribution'''
#solar_zenith_angle =
# solar_pedersen_conductance = 0.76 * np.sqrt( * np.cos(solar_zenith_angle))
# solar_hall_conductance = 1.04 * np.sqrt( * np.cos(solar_zenith_angle))

'''Creating our output dictionary'''
output_dict = {
    "electron_energy_flux": [electron_energy_flux, {"UNITS": "ergs/cm^2-s", "DEPEND_0": "Epoch"}],
    "electron_average_energy": [average_electron_energy, {"UNITS": "keV", "DEPEND_0": "Epoch"}],
    "ion_energy_flux": [ion_energy_flux, {"UNITS": "ergs/cm^2-s", "DEPEND_0": "Epoch"}],
    "ion_average_energy": [average_ion_energy, {"UNITS": "keV", "DEPEND_0": "Epoch"}],
    "electron_pedersen_conductance": [electron_pedersen_conductance, {"UNITS": "S", "DEPEND_0": "Epoch"}],
    "electron_hall_conductance": [electron_hall_conductance, {"UNITS": "S", "DEPEND_0": "Epoch"}],
    "Epoch": [Epoch, {"UNITS": "s"}]
}
output_file = rf"C:/Users/jason/OneDrive/Documents/TRACERS/Science/Ionospheric_Conductance_{date}"
stl.outputCDFdata(output_file, output_dict)