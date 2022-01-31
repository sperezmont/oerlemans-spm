import numpy as np


def ice_thickness(hx_model, R, x, mu):
    if hx_model == 'plastic':
        h_ice = np.sqrt(mu * (R - x))

    return h_ice


def z_profile(hx_model, d, R, x, mu):
    if hx_model == 'plastic':
        z_srf = d + ice_thickness(hx_model, R, x, mu)

    return z_srf
