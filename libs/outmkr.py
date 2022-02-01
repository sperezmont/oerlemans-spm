import netCDF4 as nc
import numpy as np


def mk_nc_file(file_name, dimnames, dimdata, dimunits, dimlens):
    fn = file_name
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    for i in range(len(dimnames)):
        dim = ds.createDimension(dimnames[i], dimlens[i])
        dimvar = ds.createVariable(dimnames[i], 'f4', (dimnames[i],))
        dimvar.units = dimunits[i]
        dimvar[:] = dimdata[i]

    return ds


def add_data1D(ds, names, data, units, dimname):
    for i in range(len(names)):
        var = ds.createVariable(names[i], 'f4', (dimname,))
        var.units = units[i]
        var[:] = data[i]


def add_data2D(ds, names, data, units, dimnames):
    for i in range(len(names)):
        var = ds.createVariable(names[i], 'f4', (dimnames[0], dimnames[1],))
        var.units = units[i]
        var[:] = data[i]


def add_data3D(ds, names, data, units, dimnames):
    for i in range(len(names)):
        var = ds.createVariable(
            names[i], 'f4', (dimnames[0], dimnames[1], dimnames[2],))
        var.units = units[i]
        var[:] = data[i]
