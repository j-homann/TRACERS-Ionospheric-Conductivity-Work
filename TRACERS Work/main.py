# Imports
import spaceToolsLib as stl
import numpy as np
from scipy.integrate import simpson

# Loading the Data File
file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\l2\ts2_l2_ace_def_20251231_v0.10.0.cdf"
data_dict = stl.loadDictFromFile(file)
print(data_dict.keys())
print(np.shape(data_dict['ts2_l2_ace_def'][0]))

# Getting the Data
# Energy = data_dict['VARIABLE NAME HERE'][0]
# phi = data_dict['VARIABLE NAME HERE'][0]
# theta = data_dict['VARIABLE NAME HERE'][0]
# differential_energy_flux = data_dict[]

# # Calculating Energy Flux into the Ionosphere
# I_theta = simpson(np.cos, theta, axis=0)
# I_phi   = simpson(I_theta, phi, axis=0)
# I_total = simpson(I_phi, E)