#  Python libraries
import os
import sys
import netCDF4 as nc
import numpy as np

# Model libraries
import params
from libs import ice_parameters as ips
from libs import ice_profile as ip
from libs import ice_volume as iv
from libs import ice_transient as it
from libs import outmkr as outmkr

# Parameters
R, rstep, s, d0, mu0, c = params.R, params.rstep, params.s, params.d0, params.mu0, params.c
rhoi, rhow, rhob = params.rhoi, params.rhow, params.rhob

beta, A0, f = params.beta, params.A0, params.f
R0, dt, hE_step = params.R0, params.dt, params.hE_step

eta = params.eta

mu = ips.mu(mu0, c, s)

# First, we calculate the diagnostic variables
print('--> Calculating diagnostic variables ... ')
h, d, marine, rgr, rc, r = ip.profile(R, s, d0, mu, rstep)   # ice profile

V, Vsea, Vtot, r = iv.volume(
    R, marine, rc, s, d0, mu, rhoi=rhoi, rhow=rhow, rhob=rhob, rstep=50)

# Second, we calculate the transient variables
print('--> Transient simulation is now in progress ... ')
hE = np.arange(-5*d0, 5*(d0 + hE_step), hE_step)
trans_list, trans_list2, gl_list, gl_list2, ic_type_list, ic_type_list2 = [], [], [], [], [], []
for i in hE:
    transnostic, gl, ic_type = it.transient(
        R0*1000, s, d0, mu, dt, i, rhoi, rhow, rhob, beta, A0, eta, f)
    transnostic2, gl2, ic_type2 = it.transient(
        1e-5, s, d0, mu, dt, i, rhoi, rhow, rhob, beta, A0, eta, f)
    trans_list.append(transnostic/1000)
    gl_list.append(gl)
    ic_type_list.append(ic_type)
    trans_list2.append(transnostic2/1000)
    gl_list2.append(gl2)
    ic_type_list2.append(ic_type2)

trans_list, gl_list, ic_type_list = np.array(
    trans_list), np.array(gl_list), np.array(ic_type_list)
trans_list2, gl_list2, ic_type_list2 = np.array(
    trans_list2), np.array(gl_list2), np.array(ic_type_list2)

# Now we save the results
print('--> Saving results ...')
diagnostic = [h, d, rgr, rc, marine, Vtot, V, Vsea]
names = ['h(r)', 'd(r)', 'rgr(R)', 'rc(R)',
         'marine', 'Vtot(R)', 'V(R)', 'Vsea(R)']
units = ['m', 'm', 'km', 'km', '', 'km3', 'km3', 'km3']

outmkr.mk_file_multiple(diagnostic, names, units, r, 'km', 'r',
                        os.getcwd()+'/oerlemans_diagnostic.nc')

transient_hE = [trans_list, trans_list2, gl_list,
                gl_list2, ic_type_list, ic_type_list2]
names = ['Req(hE, R0)', 'Req(hE, 0)', 'GL(hE, R0)', 'GL(hE, 0)',
         'IceSheetType(R0)', 'IceSheetType(0)']
units = ['km', 'km', 'km', 'km', '', '']

outmkr.mk_file_multiple(transient_hE, names, units, hE, 'm', 'hE',
                        os.getcwd()+'/oerlemans_transient.nc')
