import netCDF4 as nc
import numpy as np
import os


def mk_file(data1, name1, units1, data2, name2, units2, dimname, file_name):
    fn = file_name
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    dim = ds.createDimension(dimname, None)

    var1 = ds.createVariable(name1, 'f4', (dimname,))
    var1.units = units1
    var1[:] = data1

    var2 = ds.createVariable(name2, 'f4', (dimname,))
    var2.units = units2
    var2[:] = data2

    ds.close()


def mk_file_multiple(data, names, units, hdata, hunits, dimname, file_name):
    fn = file_name
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    dim = ds.createDimension(dimname, None)
    hvar = ds.createVariable(dimname, 'f4', (dimname,))
    hvar.units = hunits
    hvar[:] = hdata

    for i in range(len(names)):
        var = ds.createVariable(names[i], 'f4', (dimname,))
        var.units = units[i]
        var[:] = data[i]

    ds.close()
