import numpy as np


def vol2sle(data, rhoi=0.9167, rhow=1, A_oc=3.618*10**8):
    ''' Transforms volume data to m SLE \n
        [data] = km**3 
        rhow = 1 Gt/m3 -> "disregarding the minor salinity/density effects of mixing fresh meltwater with seawater"
            More about: https://sealevel.info/conversion_factors.html
        rhow(sea water) = 1.027 Gt/m3
    '''
    SLE = rhoi/rhow * 1e3 / A_oc * data
    return SLE
