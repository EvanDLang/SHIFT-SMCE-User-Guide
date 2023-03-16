Raster Operations
=================

Reprojection and Clipping
-------------------------

There are several methods for reprojecting raster data. This notebook provides examples for using the Shift Python Utilities library(SPU) and gdalwarp.

Reprojection is a very memory intensive task and can take along time to execute. When performing this task it is recommended that you select the largest instance option inorder to have enough memory. In testing SPU(which uses rasterio) was the most performant for very large files. However, even though gdalwarp took longer it can be more reliable. It has more functionality and flexibility and will always carry out the correct order of operations. 

SHIFT Python Utilities Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SPU is an internally maintained library which provides tools for common data operations and is currently under active development.

Documentation can be found  `here`_

    .. _here: https://shift-python-utilities.readthedocs.io/en/latest/index.html

::

    from shift_python_utilities.raster_utilities import reproject_raster, clip_raster
    import geopandas as gpd

    # Read in shapefile
    geodf = gpd.read_file(shapefile)
    
    # reproject dataframe to the appropriate CRS
    geodf = geodf.to_crs(geodf.estimate_utm_crs(datum_name='WGS 84'))

    # clip the raster with the geodataframe
    clip_raster(input_raster, geodf, output_raster)

    # reproject the raster 
    reproject_raster(output_raster, out_path, crs, resampling_method, resolution)

gdalwarp
^^^^^^^^

Common Arguments:

- -of: Output file type
- -t_srs: Target spatial reference
- -tr: Target resolution
- -r: Resampling method
- -cutline: Inputfile used for cropping
- -crop_to_cutline: Crops the output to the cutline
- -overwrite: Overwrite the output_file if it exisits already 

See the `documentation`_ for more information.

    .. _documentation: https://gdal.org/programs/gdalwarp.html

From the command line:

::

    gdalwarp <input_file> <output_file> -of envi -tr 30 -30 -cutline <shapefile> -crop_to_cutline -overwrite


Rioxarray 
^^^^^^^^^

Rioxarray can also be used for reprojection and clipping, however it was found to be the slowest and often would timeout when working with very large data.

::

    import rioxarray as rxr

    # Open the input file
    ds = rxr.open_rasterio(input_file)
    
    # Clip with the shapefile
    clipped = ds.rio.clip(geodf.geometry.values, all_touched=True)

    # For larger files Rioxarray recommends using the from disk argument to prevent 
    #the entire file from being loaded into memory. In testing it was found that even 
    #with from_disk=True, the code would time out
    clipped = ds.rio.clip(geodf.geometry.values, all_touched=True, from_disk=True)