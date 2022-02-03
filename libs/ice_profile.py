import numpy as np


def ice_thickness(hx_model, R, x, mu):
    ''' Ice thickness '''
    if hx_model == 'plastic':
        h_ice = np.sqrt(mu * np.abs(R - x))  # shut warnings

    return h_ice


def z_profile(hx_model, d, R, x, mu):
    ''' Ice surface elevation '''
    if hx_model == 'plastic':
        index = [j for j, v in enumerate(x) if v >= R]
        dR = d[index[0]]
        z_srf = dR + ice_thickness(hx_model, R, x, mu)

    return z_srf


def zh_calc(x, d, hx_model, R, mu):
    ''' Calculation '''
    z = z_profile(hx_model, d, R, x, mu)
    h = ice_thickness(hx_model, R, x, mu)
    index = [j for j, v in enumerate(x) if v > R]
    z[index[0]] = d[index[0]]
    h[index[0]] = d[index[0]]
    z[index[1]:] = np.NaN
    h[index[1]:] = np.NaN

    return z, h
