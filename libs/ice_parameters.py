import math
import numpy as np


def mu(mu0, c, s):
    ''' Profile parameter '''
    return mu0 + c*s**2


def calc_zE(zE_variation, zE0, zEA, t, P):
    if zE_variation == 'constant':
        zE = zE0
    elif zE_variation == 'linear':
        print('NOT IMPLEMENTED YET')
    elif zE_variation == 'sin':
        zE = zE0 - zEA*np.sin(2*math.pi*t/P)

    return zE
