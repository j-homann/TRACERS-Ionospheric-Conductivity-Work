import numpy as np
from scipy.integrate import simpson

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
    # Integrating over pitch angle, then energy
    integrand = flux * np.abs(np.sin(angle)) * np.cos(angle)
    I_angle = simpson(integrand, angle, axis=2) * (2 * np.pi)
    energy_flux = simpson(I_angle, energy, axis=1)
    return energy_flux

def compute_average_energy(flux, energy, angle, energy_flux):
    # Reshaping energy so energy * flux doesn't throw an error
    energy_reshaped = energy[np.newaxis, :, np.newaxis]

    # Integrating over pitch angle, then energy
    integrand = energy_reshaped * flux * np.abs(np.sin(angle)) * np.cos(angle)
    I_angle = simpson(integrand, angle, axis=2) * (2 * np.pi)
    average_energy_flux = simpson(I_angle, energy, axis=1)
    average_energy = average_energy_flux / energy_flux
    return average_energy