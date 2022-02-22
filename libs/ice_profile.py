import numpy as np


def ice_thickness(hx_model, r, x, mu):
    ''' Ice thickness '''
    if hx_model == 'plastic':
        h_ice = np.sqrt(mu * np.abs(r - x))  # shut warnings

    return h_ice


def z_profile(hx_model, d, r, x, mu):
    ''' Ice surface elevation '''
    if hx_model == 'plastic':
        #index = [j for j, v in enumerate(x) if v >= r]

        z_srf = d + ice_thickness(hx_model, r, x, mu)

    return z_srf


def zh_calc(x, d, hx_model, r, mu):
    ''' Calculation '''
    z = z_profile(hx_model, d, r, x, mu)
    h = ice_thickness(hx_model, r, x, mu)
    index = [j for j, v in enumerate(x) if v >= r]
    if x[index[0]] == r:
        z[index[0]] = d[index[0]]
        z[index[1]:] = np.NaN
        h[index[1]:] = np.NaN
    else:
        z[index[0]:] = np.NaN
        h[index[0]:] = np.NaN

    return z, h
