import numpy as np


def vol2sle(data, rhoi=0.9167, rhow=1.027, A_oc=3.618*10**8):
    ''' Transforms volume data to m SLE \n
        [data] = km**3 
    '''
    SLE = rhoi/rhow * 1e3 / A_oc * data
    return SLE
