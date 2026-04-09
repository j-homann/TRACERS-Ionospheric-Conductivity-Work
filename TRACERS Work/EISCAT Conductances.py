import numpy as np
from scipy.integrate import simpson
import spaceToolsLib as stl
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Loading in the data
file = rf"C:\Users\jason\OneDrive\Documents\EISCAT\MAD6400_2026-01-15_othia_60@42m.cdf"
data_dict = stl.loadDictFromFile(file)
electron_density = data_dict['ne'][0]
ion_temperature = data_dict['ti'][0]
electron_temperature = data_dict['tr'][0] * ion_temperature
v_in = data_dict['co'][0]
alt = data_dict['range'][0]
time = data_dict['timestamps'][0]
time = [dt.datetime.utcfromtimestamp(t) for t in time]

fig, axes = plt.subplots(3, 1, sharex=True)

# Electron density
pcm1 = axes[0].pcolormesh(time, alt, electron_density.T, shading='auto', vmin = 1e10, vmax = 1e12, norm = 'log', cmap = stl.apl_rainbow_black0_cmap())
cbar = fig.colorbar(pcm1, ax=axes[0], label='e- Density (m^-3)')
axes[0].set_ylabel('Range (km)')
axes[0].set_title('Electron Density')

# Electron temperature
pcm3 = axes[1].pcolormesh(time, alt, electron_temperature.T, shading='auto', vmin = 0, vmax = 4000, cmap = stl.apl_rainbow_black0_cmap())
fig.colorbar(pcm3, ax = axes[1], label = 'e- Temperature (K)')
axes[1].set_ylabel('Range (km)')
axes[1].set_title('Electron Temperature')

# Ion temperature
pcm2 = axes[2].pcolormesh(time, alt, ion_temperature.T, shading='auto', vmin = 0, vmax = 3000, cmap = stl.apl_rainbow_black0_cmap())
fig.colorbar(pcm2, ax = axes[2], label = 'Ion Temperature (K)')
axes[2].set_ylabel('Range (km)')
axes[2].set_title('Ion Temperature')

# Shared time axis
axes[2].set_xlabel('Time')
axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()