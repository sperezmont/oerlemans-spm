import numpy as np


def profile(R, s, d0, mu, rstep=50, eta=0):
    ''' Returns h(s, r) [m] as in Oerlemans 2003 from 0 to R with a step=rstep [km]'''
    ''' Also returns: '''
    '''     marine  -> if the ice sheet is marine-based or not [True/False] '''
    '''     d       -> bed profile [m] '''
    '''     rgr     -> grounding line [km] '''
    '''     rc      -> critical radio [km] '''
    ''' R is the maximum radius of the ice sheet [km] '''
    ''' s is the bed slope '''
    ''' d0 is the central bed elevation [m] '''
    ''' mu0 and c are profile parameters [m**1/2] '''
    ''' eta is the sea level '''

    r = np.arange(0, R, rstep)*1e3

    h = d0 - s*R*1e3 + np.sqrt(mu*(R*1e3-r))
    rc = (d0 - eta)/s * 1e-3
    d = d0 - s*r

    if rc < R:
        marine = True
        rgr = (R*1e3 - 1/mu * (s*R*1e3 - d0)**2)/1e3
    else:
        marine = False
        rgr = R

    return h, d, marine, rgr, rc, r
