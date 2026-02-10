# Imports
import spaceToolsLib as stl
import numpy as np
from scipy.integrate import simpson
import tqdm

# Loading the Data File
file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\l3\ts2_l3_ace_pitch-angle-dist-pre_20251231_v0.2.0.cdf"
data_dict = stl.loadDictFromFile(file)
print(data_dict.keys())

# Getting the Data
differential_energy_flux = data_dict['ts2_l3_ace_pitch_def'][0]
Energy = data_dict['ts2_l3_ace_energy'][0]
pitch_angle = data_dict['ts2_l3_ace_pitch_angle'][0]
Epoch = data_dict['Epoch'][0]

# Calculating Energy Flux
flux = []
for i in tqdm.tqdm((range(len(Epoch)))):
    for j in range(len(pitch_angle)):
        I_Energy = simpson(differential_energy_flux[i,:,j], Energy)
        I_Theta= simpson(I_Energy*np.sin(pitch_angle), pitch_angle)
        flux.append(2*np.pi*I_Energy*I_Theta)

# Calculating ???
energy_flux = []
for i in tqdm.tqdm((range(len(Epoch)))):
    for j in range(len(pitch_angle)):
        I_Energy = simpson(Energy*differential_energy_flux[i,:,j], Energy)
        I_Theta= simpson(I_Energy*np.sin(pitch_angle), pitch_angle)
        energy_flux.append(2*np.pi*I_Energy*I_Theta)