import numpy as np
from scipy.integrate import simpson
import spaceToolsLib as stl

'''Pre-defined toggles for our data'''
# What day we are examining
date = 20250927

# Electron energy limits based on (Robinson et al., 1987)
electron_energy_min = 500       # eV
electron_energy_max = 15000     # eV

# Ion energy limits based on (Galand & Richmond, 2001)
ion_energy_min = 2000       # eV
ion_energy_max = 40000      # eV

# Only counting precipitating (downward) flux
pitch_angle_min = 0
pitch_angle_max = np.pi / 2

'''Loading files and data'''
# Loading the data files
ace_file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\ACE\l3\ts2_l3_ace_pitch-angle-dist_{date}_v1.0.0.cdf"
aci_file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\ACI\l2\ts2_l2_aci_ipd_{date}_v1.0.0.cdf"

# Defining our data dictionary
data = {
    'ACE': stl.loadDictFromFile(ace_file),
    'ACI': stl.loadDictFromFile(aci_file)
}

'''Defining some recurring functions'''
def restrict_energy_range(energy, flux, energy_min, energy_max):
    mask = (energy >= energy_min) & (energy <= energy_max)
    energy = energy[mask]
    flux = flux[:, mask, :]
    return energy, flux

def restrict_angle_range(angle, flux, angle_min, angle_max):
    mask = (angle >= angle_min) & (angle <= angle_max)
    angle = angle[mask]
    flux = flux[:, :, mask]
    return angle, flux

def compute_energy_flux(flux, energy, angle):
    integrand = flux * np.sin(angle) * np.cos(angle)

    # Integrating over pitch angle first, then energy
    I_angle = simpson(integrand, angle, axis=2) * (2 * np.pi)
    energy_flux = simpson(I_angle, energy, axis=1)
    return energy_flux

def compute_average_energy(flux, energy, angle, energy_flux):
    # Reshaping energy so energy * flux doesn't throw an error
    energy_reshaped = energy[np.newaxis, :, np.newaxis]

    integrand = energy_reshaped * flux * np.sin(angle) * np.cos(angle)

    # Integrating over angle, then energy
    I_angle = simpson(integrand, angle, axis=2) * (2 * np.pi)
    average_energy_flux = simpson(I_angle, energy, axis=1)
    average_energy = average_energy_flux / energy_flux
    return average_energy

'''Electron Contribution'''
# Getting ACE data
ace_def = data['ACE']['ts2_l3_ace_pitch_def'][0] # eV / eV cm^2 sr s
ace_energy = data['ACE']['ts2_l3_ace_energy'][0]
ace_pitch = np.deg2rad(data['ACE']['ts2_l3_ace_pitch_angle'][0]) # Converted from degrees to radians

# Restrict pitch angle and energy based off our defined limits
ace_pitch, ace_def = restrict_angle_range(ace_pitch, ace_def, pitch_angle_min, pitch_angle_max)
ace_energy, ace_def = restrict_energy_range(ace_energy, ace_def, electron_energy_min, electron_energy_max)

# Remove negative values
ace_def = np.clip(ace_def, 0.01, None)

# Flip energy axis to avoid negative values in integration
ace_energy = np.flip(ace_energy)
ace_def = np.flip(ace_def, axis=1)

# Energy flux
electron_energy_flux = compute_energy_flux(ace_def, ace_energy, ace_pitch)

# Average Energy
average_electron_energy = compute_average_energy(ace_def, ace_energy, ace_pitch, electron_energy_flux)
average_electron_energy /= 1000   # Converted from eV to keV

# Electron Pedersen and Hall Conductances
electron_pedersen_conductance = ((40 * average_electron_energy /(16 + average_electron_energy**2))
                                 * np.sqrt(electron_energy_flux))
electron_hall_conductance = 0.45 * average_electron_energy**0.85 * electron_pedersen_conductance

'''Ion Contribution'''
# Getting ACI data
aci_def = data['ACI']['ts2_l2_aci_tscs_def'][0]
aci_energy = data['ACI']['ts2_l2_aci_energy'][0]
aci_angle = np.deg2rad(data['ACI']['ts2_l2_aci_look_angle'][0]) # Converted from degrees to radians

print(aci_energy)

# Restrict angle and energy based off our defined limits
aci_angle, aci_def = restrict_angle_range(aci_angle, aci_def, pitch_angle_min, pitch_angle_max)
aci_energy, aci_def = restrict_energy_range(aci_energy, aci_def, ion_energy_min, ion_energy_max)

# Flip energy if necessary
aci_energy = np.flip(aci_energy)
aci_def = np.flip(aci_def, axis=1)

# Ion energy flux
ion_energy_flux = compute_energy_flux(aci_def, aci_energy, aci_angle)

# Ion characteristic energy
average_ion_energy = compute_average_energy(aci_def, aci_energy, aci_angle, ion_energy_flux)
average_ion_energy /= 1000   # Converted from eV to keV

'''Creating our output dictionary'''
output_dict = {
    "electron_energy_flux": [electron_energy_flux, {"UNITS": "ergs/cm^2-s", "DEPEND_0": "Epoch"}],
    "electron_average_energy": [average_electron_energy, {"UNITS": "keV", "DEPEND_0": "Epoch"}],
    "ion_energy_flux": [ion_energy_flux, {"UNITS": "ergs/cm^2-s", "DEPEND_0": "Epoch"}],
    "ion_characteristic_energy": [average_ion_energy, {"UNITS": "keV", "DEPEND_0": "Epoch"}],
    "electron_pedersen_conductance": [electron_pedersen_conductance, {"UNITS": "S", "DEPEND_0": "Epoch"}],
    "electron_hall_conductance": [electron_hall_conductance, {"UNITS": "S", "DEPEND_0": "Epoch"}],
    "Epoch": [Epoch, {"UNITS": "s"}]
}
output_file = rf"C:/Users/jason/OneDrive/Documents/TRACERS/Science/Ionospheric_Conductance_{date}"
stl.outputCDFdata(output_file, output_dict)