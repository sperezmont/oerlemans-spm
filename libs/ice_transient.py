import numpy as np
import math


def calc_hR(hE, A, beta):
    return hE + A/beta


def calc_rR(r, mu, hR, d0, s):
    rR = min(r, r - 1/mu*(hR - d0 + s*r))
    rR = max(0, rR)
    return rR


def calc_rgr(r, mu, s, d0):
    rgr = max(0, r - 1/mu * (s*r - d0)**2)
    return rgr


def calc_Fgr(rgr, s, d0, eta, f, rhoi, rhow):
    ''' Flux across the grounding line, Oerlemans (2003)'''
    delta = rhow/rhoi
    return 2*math.pi*rgr*f*delta**2*(s*rgr-d0+eta)**2


def cMB(A, r, beta, hR, d0, s, rR, mu, eps1):
    ''' Continental ice-sheet mass balance, Oerlemans (2003) '''
    Btot = math.pi*A*r**2 - math.pi*beta*(hR-d0+s*r)*(r**2-rR**2) + \
        4/15*math.pi*beta*np.sqrt(mu)*(r-rR)**(3/2)*(3*rR+2*r)
    B = math.pi*(1+eps1) * (4/3*np.sqrt(mu)*r**(3/2) - s*r**2)
    if B <= 0:
        B = 1e-5
    return Btot, B


def mMB(A, r, beta, hR, rgr, d0, s, rR, mu, eps1, eps2, eta, f, rhoi, rhow):
    ''' Marine ice-sheet mass balance, Oerlemans (2003) '''
    Btot = math.pi*A*rgr**2 - math.pi*beta*(hR-d0+s*r)*(rgr**2-rR**2) + 4/15*beta*np.sqrt(
        mu)*((2*r+3*rR)*(r-rR)**(3/2) - (2*r+3*rgr)*(r-rgr)**(3/2))
    B = math.pi*(1+eps1)*(4/3*np.sqrt(mu)*r**(3/2)-s*r**2) - \
        2*eps2*math.pi*(s*r**2-d0*r)
    if B <= 0:
        B = 1e-5
    Btot = Btot - calc_Fgr(rgr, s, d0, eta, f, rhoi, rhow)
    return Btot, B


def calc_R(r, rc, hE, dt, A0, eta, f, beta, mu, d0, s, eps1, eps2, rhoi, rhow):
    hR = calc_hR(hE, A0, beta)
    rR = calc_rR(r, mu, hR, d0, s)

    if rc < r:
        marine = True
        rgr = calc_rgr(r, mu, s, d0)
        Btot, B = mMB(A0, r, beta, hR, rgr, d0, s, rR,
                      mu, eps1, eps2, eta, f, rhoi, rhow)
    else:
        marine = False
        rgr = np.NaN
        Btot, B = cMB(A0, r, beta, hR, d0, s, rR, mu, eps1)

    R = max(1e-5, r + Btot/B * dt)

    return R, rgr, marine


def transient(R0, s, d0, mu, dt, hE, rhoi, rhow, rhob, beta, A0, eta, f):
    ''' Calculates the transient evolution of the ice sheet, Oerlemans (2003) '''

    eps1 = rhoi/(rhob - rhoi)
    eps2 = rhow/(rhob - rhoi)
    rc = (d0 - eta)/s

    Ri = R0
    R, rgr, marine = calc_R(Ri, rc, hE, dt, A0, eta, f, beta,
                            mu, d0, s, eps1, eps2, rhoi, rhow)

    while np.abs(R - Ri) > 1e-5:
        R, rgr, marine = calc_R(Ri, rc, hE, dt, A0, eta, f, beta,
                                mu, d0, s, eps1, eps2, rhoi, rhow)
        Ri = R
    return R, rgr, marine
