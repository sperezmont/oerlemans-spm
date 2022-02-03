# Libraries
from numpy import ma
import numpy as np

import netCDF4 as nc

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.path as mpath

import imageio

# Load
data = nc.Dataset('oerlemans2D.nc')

time = data.variables['time'][:]
x = data.variables['x'][:]
d = data.variables['d'][:]
eta = data.variables['eta'][:]
zE = data.variables['zE'][:]
rgr = data.variables['rgr'][:]

z_srf = data.variables['z_srf'][:]
H_ice = data.variables['H_ice'][:]

R = data.variables['R'][:]
SLE = data.variables['SLE'][:]

# Activating LaTeX font
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']
rc('text', usetex=True)


# Plotting


def plotgen(t):
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(12, 8))

    ax1.plot(x, d, color='saddlebrown')
    ax1.fill_between(x, len(x)*[eta[t]], min(d), color='b')
    ax1.fill_between(x, d, min(d), color='saddlebrown')
    ax1.plot(x, z_srf[t, :], color='lightgrey')
    ax1.fill_between(x, z_srf[t, :], d, color='lightgrey')
    ax1.plot(rgr[t], 0, color='k', marker='v', markersize=10)
    ax1.set_xlabel('Distance from the center, x (km)', fontsize=18)
    ax1.set_ylabel('Ice surface elevation (m)', fontsize=18)
    ax1.set_xlim([x[0], x[-1]])
    ax1.set_ylim([min(d), np.nanmax(z_srf)])
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelsize=14)
    ax1.xaxis.set_label_position('top')
    ax1.xaxis.tick_top()

    ax2.plot(time, SLE, color='blue', linewidth=3, marker='o')
    ax2.plot(time[t], SLE[t], color='red', marker='o', markersize=10)
    ax2.set_ylabel('Volume (m SLE)', fontsize=18)
    ax2.set_xlim([time[0], time[-1]])
    ax2.set_ylim([0, 1.1*max(SLE)])
    ax2.grid(linestyle='--')
    ax2.set_xticklabels([])
    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)

    ax3.plot(time, R, color='k', linewidth=3, marker='o')
    ax3.plot(time[t], R[t], color='red', marker='o', markersize=10)
    ax3.set_xlabel('Time (yrs)', fontsize=18)
    ax3.set_ylabel('R (km)', fontsize=18)
    ax3.set_xlim([time[0], time[-1]])
    ax3.set_ylim([0, 1.1*max(R)])
    ax3.grid(linestyle='--')
    ax3.tick_params(axis='x', labelsize=14)
    ax3.tick_params(axis='y', labelsize=14)

    ax4.plot(time, zE, color='darkgrey', linewidth=3, marker='o')
    ax4.plot(time[t], zE[t], color='red', marker='o', markersize=10)
    ax4.set_xlabel('Time (yrs)', fontsize=18)
    ax4.set_ylabel('Equilibrium height (m)', fontsize=18)
    ax4.set_xlim([time[0], time[-1]])
    ax4.set_ylim([min(zE), 1.1*max(zE)])
    ax4.grid(linestyle='--')
    ax4.tick_params(axis='x', labelsize=14)
    ax4.tick_params(axis='y', labelsize=14)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


imageio.mimsave('oerlemans-plot.gif', [plotgen(i)
                                       for i in range(len(time))], fps=1.3)
plt.close()
