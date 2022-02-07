import numpy as np
from math import pi as pi


def calc_V(marine, bed_type, hx_model, R, rc, s, d0, mu, eps1, eps2):
    if bed_type == 'linear':
        if hx_model == 'plastic':
            V = 8/15*pi*np.sqrt(mu)*R**(5/2) - 1/3*pi*s*R**3
            if marine:
                Vsea = pi * (2/3*s*(R**3-rc**3) - d0*(R**2-rc**2))
            else:
                Vsea = 0
            Vtot = (1+eps1)*V - eps2*Vsea

    return Vtot, V, Vsea
