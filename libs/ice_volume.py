import numpy as np
import math


def volume(R, marine, rc, s, d0, mu, rhoi=917, rhow=1000, rhob=2700, rstep=50):
    ''' Returns V(s, R) [m] as in Oerlemans 2003 from 0 to R with a step=rstep [km3]'''
    ''' Also returns: '''
    ''' R is the maximum radius of the ice sheet [km]'''
    ''' s is the bed slope '''
    ''' d0 is the central bed elevation [m] '''
    ''' mu0 and c are profile parameters [m**1/2] '''
    ''' rhoi, rhow and rhob are the densities of ice, water and bed [kg/m3]'''

    r = np.arange(0, R, rstep)

    eps1 = rhoi/(rhob - rhoi)
    eps2 = rhow/(rhob - rhoi)

    V = (8/15*math.pi*np.sqrt(mu)*(r*1e3) **
         (5/2) - 1/3*math.pi*s*(r*1e3)**3)*1e-9

    if marine:
        Vsea = math.pi*(2/3*s*(r**3 - rc**3) *
                        1e9 - d0*(r**2 - rc**2)*1e6)*1e-9
        Vsea[r < rc] = 0
    else:
        Vsea = 0

    Vtot = (1+eps1)*V - eps2*Vsea

    return V, Vsea, Vtot, r
