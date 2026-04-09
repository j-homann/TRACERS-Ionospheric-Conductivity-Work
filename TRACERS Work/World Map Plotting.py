import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import spaceToolsLib as stl
import datetime as dt
import numpy as np

# Loading the data
file = rf"C:\Users\jason\OneDrive\Documents\TRACERS\EAD\ts2_def_ead_20260115_v0.10.0.cdf"
data_dict = stl.loadDictFromFile(file)
lat = data_dict['ts2_ead_lat_geod'][0]
lon = data_dict['ts2_ead_lon_geod'][0]
Epoch = data_dict['Epoch'][0]

# Compute longitude differences
dlon = np.abs(np.diff(lon))

# Define a threshold (e.g., 180° wrap)
jump_idx = np.where(dlon > 180)[0]

# Insert NaNs to break the line
lon = lon.astype(float).copy()
lat = lat.astype(float).copy()

for idx in jump_idx:
    lon[idx+1] = np.nan
    lat[idx+1] = np.nan

# Defining the time range for our data
start_time = dt.datetime(2026, 1, 15, 11, 20, 0)
end_time   = dt.datetime(2026, 1, 15, 11, 30, 0)

mask = (Epoch >= start_time) & (Epoch <= end_time)
lat = lat[mask]
lon = lon[mask]
Epoch = Epoch[mask]

# Defining the location of the EISCAT radar in Svalbard
EISCAT_lon = 16.05
EISCAT_lat = 78.15

# Creating the figure
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.gridlines(draw_labels=True)

# Plot TRACERS T2 trajectory
ax.plot(lon, lat, color='red', linewidth=1, transform=ccrs.PlateCarree())

# Mark start, end, and EISCAT location with points
ax.scatter(lon[0], lat[0], color='green', label='Start ROI', transform=ccrs.PlateCarree())
ax.scatter(lon[-1], lat[-1], color='blue', label='End ROI', transform=ccrs.PlateCarree())
ax.scatter(EISCAT_lon, EISCAT_lat, color='purple', label = 'EISCAT',transform=ccrs.PlateCarree(), zorder=5)

# Add labels to start, end, and EISCAT points
ax.text(lon[0], lat[0], Epoch[0].strftime("%H:%M:%S"), transform=ccrs.PlateCarree(), fontsize=8)
ax.text(lon[-1], lat[-1], Epoch[-1].strftime("%H:%M:%S"), transform=ccrs.PlateCarree(), fontsize=8)
ax.text(EISCAT_lon, EISCAT_lat, transform=ccrs.PlateCarree(), s = 50)

plt.legend()
plt.title(f"TRACERS T2 Trajectory from \n{start_time} to {end_time}")
plt.show()