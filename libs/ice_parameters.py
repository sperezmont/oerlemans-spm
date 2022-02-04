import math
import numpy as np


def mu(mu0, c, s):
    ''' Profile parameter '''
    return mu0 + c*s**2


def calc_eta(sea_level, eta0, etaA, ti, etaP):
    if sea_level == 'constant':
        return eta0
    elif sea_level == 'linear':
        print('NOT IMPLEMENTED YET')
    elif sea_level == 'sin':
        return eta0 - etaA*np.sin(2*math.pi*ti/etaP)
    elif sea_level == 'list':
        print('NOT IMPLEMENTED YET')


def calc_zE(zE_variation, zE0, zEA, ti, P):
    if zE_variation == 'constant':
        zE = zE0
    elif zE_variation == 'linear':
        print('NOT IMPLEMENTED YET')
    elif zE_variation == 'sin':
        zE = zE0 - zEA*np.sin(2*math.pi*ti/P)
    elif zE_variation == 'list':
        print('NOT IMPLEMENTED YET')

    return zE
