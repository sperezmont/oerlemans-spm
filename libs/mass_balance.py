from math import e, pi as e, pi
import numpy as np


def calcA(mode, A0, Cr=None, r=None):
    if mode == 'constant':
        A = A0
    if mode == 'exp':
        A = A0*e**(-1*r/Cr)
    return A


def calc_MB(marine, bed_type, hx_model, r, zr, d0, s, mu, A, beta, f, delta, eta):
    if marine:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                rgr = r - 1/mu * (s*r - d0)**2
                rR = r - 1/mu * (zr - d0 + s*r)**2
                Fgr = 2*pi*rgr*f*delta**2*(s*rgr-d0+eta)
                MB = pi*A*rgr**2 - pi*beta * \
                    (zr-d0+s*r)*(rgr**2-rR**2) + 4/15*pi*beta*np.sqrt(mu) * \
                    ((2*r+3*rR)*(r-rR)**(3/2) - (2*r+3*rgr)*(r-rgr)**(3/2))
                MB = MB - Fgr
                return MB, rgr
    else:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                rR = r - 1/mu * (zr - d0 + s*r)**2
                MB = pi*A*r**2 - pi*beta * \
                    (zr-d0+s*r)*(r**2-rR**2) + 4/15*pi*beta * \
                    np.sqrt(mu)*(r-rR)**(3/2)*(3*rR+2*r)
                return MB


def calc_M(marine, bed_type, hx_model, r, s, d0, mu, eps1, eps2):
    if marine:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                M = pi*(1+eps1)*(4/3*np.sqrt(mu)*r**(3/2)-s*r**2) - \
                    2*eps2*pi*(s*r**2 - d0*r)

    else:
        if bed_type == 'linear':
            if hx_model == 'plastic':
                M = pi*(1+eps1)*(4/3*np.sqrt(mu)*r**(3/2)-s*r**2)

    return M
