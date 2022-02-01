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
from libs import outmkr as outmkr

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

# Third, we calculate the bed and the domains
x = np.arange(0, domain + dx, dx)
times = np.arange(0, T + dt, dt)
d = bp.bed_profile(bed_type, x, d0, s)

# Fourth, let's calculate the time evolution
# Initialization
Revo = np.empty(len(times))
hevo = np.empty((len(times), len(x)))
zevo = np.empty((len(times), len(x)))

Revo[0] = R0
zevo[0, :], hevo[0, :] = ipf.zh_calc(x, d, hx_model, R0, mu)
# Calculation
for t in range(1, len(times)):
    R = Revo[t-1]

    if bed_type == 'linear':
        rc = (d0 - eta)/s * 1e-3

    if R >= rc:  # asses if marine ice-sheet
        marine = True
        A = mb.calcA('exp', A0, CR, R)
    else:
        marine = False
        A = mb.calcA('constant', A0)

    if Acc_model == 'linear':
        zE, beta = params.zE0, params.beta
        zR = zE + A/beta
        MB = mb.calc_MB(marine, bed_type, hx_model, R,
                        zR, d0, s, mu, A, beta, f, delta, eta)
        M = mb.calc_M(marine, bed_type, hx_model, R, s, d0, mu, eps1, eps2)

        Revo[t] = R + MB/M*dt

    # profile generation
    zevo[t, :], hevo[t, :] = ipf.zh_calc(x, d, hx_model, Revo[t], mu)

# Now we store the results on oerlemans2D.nc
dimnames, dimdata, dimunits, dimlens = ['time', 'x'], [
    times, x/1e3], ['yr', 'km'], [None, len(x)]
ds = outmkr.mk_nc_file('oerlemans2D.nc', dimnames, dimdata, dimunits, dimlens)

names1D, data1D, units1D = ['R'], [Revo/1e3], ['km']
outmkr.add_data1D(ds, names1D, data1D, units1D, dimnames[0])

names2D, data2D, units2D = ['z_srf', 'H_ice'], [zevo, hevo], ['m', 'm']
outmkr.add_data2D(ds, names2D, data2D, units2D, dimnames)

ds.close()
