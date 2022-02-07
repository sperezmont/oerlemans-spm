# Libraries
from numpy import ma
import numpy as np

import netCDF4 as nc

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.path as mpath

import imageio

from params import s, d0

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
# static parts
fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(12, 8))

# first panel
ax1.plot(x, d, color='saddlebrown', zorder=5)
ax1.fill_between(x, d, min(d), color='saddlebrown', zorder=5)
ax1.axhline(y=eta[0], color='k', linestyle='--', zorder=8)
ax1.set_xlabel('Distance to the center (km)', fontsize=18)
ax1.set_ylabel('Ice surface elevation (m)', fontsize=18)
ax1.set_xlim([x[0], x[-1]])
ax1.set_ylim([min(d), np.nanmax(z_srf)])
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
ax1.xaxis.set_label_position('top')
ax1.xaxis.tick_top()
custom_lines = [mpl.lines.Line2D([0], [0], ls='None', marker=None),
                mpl.lines.Line2D([0], [0], ls='None', marker=None)]
leg = ax1.legend(custom_lines, [
    's = '+str(s), 'd0 = '+str(d0)+' m'], loc='upper right', markerscale=0.0001, fontsize=12, handlelength=0)
leg._legend_box.align = 'left'
leg.get_title().set_fontsize('14')

# second panel
ax2.plot(time, SLE, color='dodgerblue', linewidth=3)
ax2.set_ylabel('Ice volume (m SLE)', fontsize=18)
ax2.set_ylim([0.9*min(SLE), 1.1*max(SLE)])
ax2.grid(linestyle='--')
ax2.set_xticklabels([])
ax2.tick_params(axis='x', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)

# third panel
ax3.plot(time, R, color='lightslategrey', linewidth=3, label='R')
ax3.plot(time, rgr, color='olive', linewidth=2.8, label=r'$r_{gr}$')
ax3.set_xlabel('Time (yrs)', fontsize=18)
ax3.set_ylabel('Distance to the center (km)', fontsize=18)
ax3.set_ylim([0.9*min(R), 1.1*max(R)])
ax3.grid(linestyle='--')
ax3.tick_params(axis='x', labelsize=14)
ax3.tick_params(axis='y', labelsize=14)
ax3.legend(fontsize=14)

# fourth panel
lns1 = ax4.plot(time, zE, color='indigo', linewidth=5, label=r'$z_E$')
ax4.set_xlabel('Time (yrs)', fontsize=18)
ax4.set_ylabel('Equilibrium height (m)', fontsize=18)
ax44 = ax4.twinx()
lns2 = ax44.plot(time, eta, color='lightblue',
                 linewidth=3, label=r'$\eta$')
ax44.set_ylabel('Sea-level (m)', rotation=270, labelpad=15, fontsize=18)
ax4.grid(axis='x', linestyle='--')
ax4.tick_params(axis='x', labelsize=14)
ax4.tick_params(axis='y', labelsize=14)
ax44.tick_params(axis='y', labelsize=14)
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax44.legend(lns, labs, fontsize=14)

# non-static parts


def remove_lines(line2remove):
    line = line2remove.pop(0)
    line.remove()


def plotgen(t):

    # first panel
    sea = ax1.fill_between(
        x, len(x)*[eta[t]], min(d), color='lightblue', zorder=0)
    ice_line = ax1.plot(x, z_srf[t, :], color='lightgrey')
    ice_cont = ax1.fill_between(x, z_srf[t, :], d, color='lightgrey')
    index = [j for j, v in enumerate(x) if v >= R[t]]
    drgr = d[index[0]]
    if drgr <= eta[t]:
        rgr_point = ax1.plot(
            rgr[t], 1.6*drgr, color='olive', marker='^', markersize=10, zorder=9)
    zE_point = ax1.plot(1.2*R[t], zE[t], color='indigo',
                        marker='<', markersize=10, zorder=10)

    # second panel
    sle_point = ax2.plot(time[t], SLE[t], color='red',
                         marker='o', markersize=10)

    # third panel
    R_point = ax3.plot(time[t], R[t], color='red', marker='o', markersize=10)
    rgr3_point = ax3.plot(time[t], rgr[t], color='red',
                          marker='o', markersize=8)

    # fourth panel
    ze4_point = ax4.plot(time[t], zE[t], color='red',
                         marker='o', markersize=10)
    eta_point = ax44.plot(time[t], eta[t], color='red',
                          marker='o', markersize=10)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    remove_lines(ice_line)
    sea.remove()
    ice_cont.remove()
    remove_lines(zE_point)
    if drgr <= eta[t]:
        remove_lines(rgr_point)
    remove_lines(sle_point)
    remove_lines(R_point)
    remove_lines(rgr3_point)
    remove_lines(ze4_point)
    remove_lines(eta_point)
    return image


imageio.mimsave('oerlemans-plot.gif', [plotgen(i)
                                       for i in range(len(time))], fps=1.3)
plt.close()
