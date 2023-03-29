import netCDF4
import numpy as np
from spectral.io import envi
import os

envi_typemap = {
    'uint8': 1,
    'int16': 2,
    'int32': 3,
    'float32': 4,
    'float64': 5,
    'complex64': 6,
    'complex128': 9,
    'uint16': 12,
    'uint32': 13,
    'int64': 14,
    'uint64': 15
}


# path to the netcdf file
file = "path_to_netcdf_file"

# The name of the data variable ex. reflectance, radiance, band
data_var = "reflectance"

# Then name of the band dimension ex. wavelength, band
band_name = 'wavelength',

# Output file name
output_name = os.path.splitext(input_path)[0]

# load the data
nc_ds = netCDF4.Dataset(input_path, 'r', format='NETCDF4')

# retrieve the data variable of interest
ds = nc_ds[data_var]

# format your metadata
# this will be very specific to your data
metadata = {
    'lines':  nc_ds[data_var].shape[0],
    'samples': nc_ds[data_var].shape[1],
    'bands':  nc_ds[data_var].shape[2],
    'interleave': 'bsq',
    'header offset' : 0,
    'file type' : 'ENVI Standard',
    'data type' : envi_typemap[str(nc_ds[data_var].dtype)],
    'byte order' : 0
}

# Insert you own map data based of the transform and crs
metadata['map info'] = '{Arbitrary, 1, 1, 90, -180, 0.5, 0.5, 0, North, rotation=180}'

# retrieve the list of wavelengths
metadata['wavelength'] = nc_ds.variables[band_name][:].astype(str).tolist()

# create the output ENVI file and write the data
envi_ds = envi.create_image(envi_header(output_name), metadata, ext='', force=True) 
mm = envi_ds.open_memmap(interleave='bip', writable=True)
mm[...] = np.array(nc_ds[ds])
del mm, envi_ds