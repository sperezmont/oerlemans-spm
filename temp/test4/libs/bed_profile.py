import numpy as numpy


def bed_profile(bed_type, r, d0, s):
    if bed_type == 'linear':
        d = d0 - s*r
    return d
