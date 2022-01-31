#  Python libraries
import matplotlib.pyplot as plt
import os
import sys
import netCDF4 as nc
import numpy as np

# Model libraries
import params
from libs import ice_parameters as ips
from libs import bed_profile as bp
from libs import mass_balance as mb
from libs import ice_profile as ipf

# First, asses the parameter settings
bed_type = params.bed_type

hx_model = params.hx_model
geo_model = params.geo_model

sea_level = params.sea_level

Acc_model = params.Acc_model

# Now, we load the variables we need
# BED PROFILE
if bed_type == 'linear':
    d0, s = params.d0, params.s

# MATERIAL APROXIMATION
if hx_model == 'plastic':
    if geo_model == 'oerlemans2003':
        mu0, c, s = params.mu0, params.c, params.s
        mu = ips.mu(mu0, c, s)

# Second, we load the initial conditions
domain, zdomain, dx, dz = params.domain * \
    1e3, params.zdomain, params.dx * 1e3, params.dz
dt, T = params.dt, params.T
R0 = params.R0 * 1e3
A0, CR = params.A0, params.CR * 1e3

rhoi, rhow, rhob = params.rhoi, params.rhow, params.rhob
f = params.f
eps1, eps2, delta = rhoi/(rhob-rhoi), rhow/(rhob-rhoi), rhow/rhoi

if sea_level == 'constant':
    eta = params.eta0

# Third, we calculate the bed
x = np.arange(0, domain + dx, dx)
d = bp.bed_profile(bed_type, x, d0, s)

# Fourth, let's calculate the time evolution
times = np.arange(0, T + dt, dt)
y = np.arange(0, zdomain + dz, dz)
Revo = np.empty(len(times))
hevo = np.empty((len(times), len(y), len(x)))
zevo = np.empty((len(times), len(y), len(x)))

Revo[0] = R0
for t in range(1, len(times)):

    R = Revo[t-1]

    zevo[t, :, :] = ipf.z_profile(hx_model, d, R, x, mu)
    hevo[t, :, :] = ipf.ice_thickness(hx_model, R, x, mu)

    if bed_type == 'linear':    # asses if marine ice-sheet
        rc = (d0 - eta)/s * 1e-3

    if R >= rc:
        marine = True
    else:
        marine = False

    if marine:  # A calculation
        A = mb.calcA('exp', A0, CR, R)
    else:
        A = mb.calcA('constant', A0)

    if Acc_model == 'linear':
        zE, beta = params.zE0, params.beta
        zR = zE + A/beta
        MB = mb.calc_MB(marine, bed_type, hx_model, R,
                        zR, d0, s, mu, A, beta, f, delta, eta)
        M = mb.calc_M(marine, bed_type, hx_model, R, s, d0, mu, eps1, eps2)

        Revo[t] = R + MB/M*dt

plt.plot(zevo[0, :, :])
plt.show()
