from math import e, pi as e, pi
import numpy as np


def calcA(mode, A0, CR=None, R=None):
    if mode == 'constant':
        A = A0
    if mode == 'exp':
        A = A0*e**(-R/CR)
    return A


def calc_MB(marine, bed_type, hx_model, R, zR, d0, s, mu, A, beta, f, delta, eta):
    if marine:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                rgr = R - 1/mu * (s*R - d0)**2
                rR = R - 1/mu * (zR - d0 + s*R)**2
                Fgr = 2*pi*rgr*f*delta**2*(s*rgr-d0+eta)
                MB = pi*A*rgr**2 - pi*beta * \
                    (zR-d0+s*R)*(rgr**2-rR**2) + 4/15*pi*beta*np.sqrt(mu) * \
                    ((2*R+3*rR)*(R-rR)**(3/2) - (2*R+3*rgr)*(R-rgr)**(3/2))
                MB = MB - Fgr
    else:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                rR = R - 1/mu * (zR - d0 + s*R)**2
                MB = pi*A*R**2 - pi*beta * \
                    (zR-d0+s*R)*(R**2-rR**2) + 4/15*pi*beta * \
                    np.sqrt(mu)*(R-rR)**(3/2)*(3*rR+2*R)
    return MB


def calc_M(marine, bed_type, hx_model, R, s, d0, mu, eps1, eps2):
    if marine:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                M = pi*(1+eps1)*(4/3*np.sqrt(mu)*R**(3/2)-s*R**2) - \
                    2*eps2*pi*(s*R**2 - d0*R)

    else:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                M = pi*(1+eps1)*(4/3*np.sqrt(mu)*R**(3/2)-s*R**2)

    return M
