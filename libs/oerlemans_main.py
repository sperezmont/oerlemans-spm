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
from libs import ice_volume as iv
from libs import misc as misc
from libs import outmkr as outmkr

# First, asses the parameter settings
bed_type = params.bed_type
hx_model = params.hx_model
geo_model = params.geo_model
sea_level = params.sea_level
Acc_model = params.Acc_model
zE_variation = params.zE_variation


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
zE0, zEA, P = params.zE0, params.zEA, params.P

rhoi, rhow, rhob = params.rhoi, params.rhow, params.rhob
A_oc = params.A_oc
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
Vtot_evo, V_evo, Vsea_evo = np.empty(
    len(times)), np.empty(len(times)), np.empty(len(times))
is_kind, eta_evo = np.empty(len(times)), np.empty(len(times))

if bed_type == 'linear':
    rc = (d0 - eta)/s
    if R0 >= rc:  # asses if marine ice-sheet
        marine = True
    else:
        marine = False
Revo[0] = R0
zevo[0, :], hevo[0, :] = ipf.zh_calc(x, d, hx_model, R0, mu)
# isostasy contribution
if marine:
    zevo[0, :] = (1+eps1)*zevo[0, :] + eps2*(eta - d)
    hevo[0, :] = (1+eps1)*hevo[0, :] + eps2*(eta - d)
else:
    zevo[0, :] = (1+eps1)*hevo[0, :]
    hevo[0, :] = (1+eps1)*hevo[0, :]

Vtot_evo[0], V_evo[0], Vsea_evo[0] = iv.calc_V(marine, bed_type, hx_model,
                                               R0, rc, s, d0, mu, eps1, eps2)
is_kind[0], eta_evo[0] = marine, eta

# Calculation
for t in range(1, len(times)):
    R = Revo[t-1]

    if bed_type == 'linear':
        rc = (d0 - eta)/s

    if R >= rc:  # asses if marine ice-sheet
        marine = True
        A = mb.calcA('exp', A0, CR, R)
    else:
        marine = False
        A = mb.calcA('constant', A0)

    zE = ips.calc_zE(zE_variation, zE0, zEA, times[t], P)

    if Acc_model == 'linear':
        beta = params.beta
        zR = zE + A/beta
        MB = mb.calc_MB(marine, bed_type, hx_model, R,
                        zR, d0, s, mu, A, beta, f, delta, eta)
        M = mb.calc_M(marine, bed_type, hx_model, R, s, d0, mu, eps1, eps2)

        Revo[t] = R + MB/M*dt

    # profile generation
    zevo[t, :], hevo[t, :] = ipf.zh_calc(x, d, hx_model, Revo[t], mu)

    # isostasy contribution
    if marine:
        zevo[t, :] = (1+eps1)*zevo[t, :] + eps2*(eta - d)
        hevo[t, :] = (1+eps1)*hevo[t, :] + eps2*(eta - d)
    else:
        zevo[t, :] = (1+eps1)*hevo[t, :]
        hevo[t, :] = (1+eps1)*hevo[t, :]

    # Volume calculation
    Vtot_evo[t], V_evo[t], Vsea_evo[t] = iv.calc_V(marine, bed_type, hx_model,
                                                   Revo[t], rc, s, d0, mu, eps1, eps2)
    is_kind[t], eta_evo[t] = marine, eta


# Now we calculate some variables
SLE = misc.vol2sle(Vtot_evo/1e9, rhoi=rhoi, rhow=rhow, A_oc=A_oc)

# Now we store the results in oerlemans2D.nc
dimnames, dimdata, dimunits, dimlens = ['time', 'x'], [
    times, x/1e3], ['yr', 'km'], [None, len(x)]
ds = outmkr.mk_nc_file('oerlemans2D.nc', dimnames, dimdata, dimunits, dimlens)

outmkr.add_data1D(ds, ['d'], [d], ['m'], dimnames[1])

names1D, data1D, units1D = ['R', 'Vtot', 'V', 'Vsea', 'SLE', 'Ice Sheet type', 'eta'], [
    Revo/1e3, Vtot_evo/1e9, V_evo/1e9, Vsea_evo/1e9, SLE, is_kind, eta], ['km', 'km3', 'km3', 'km3', 'm SLE', 'Marine/Continental', 'm']
outmkr.add_data1D(ds, names1D, data1D, units1D, dimnames[0])

names2D, data2D, units2D = ['z_srf', 'H_ice'], [zevo, hevo], ['m', 'm']
outmkr.add_data2D(ds, names2D, data2D, units2D, dimnames)

ds.close()
