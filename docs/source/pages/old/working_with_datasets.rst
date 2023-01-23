=====================
Working With Datasets
=====================

All of the SHIFT AVIRIS-NG data lives in the dh-shift-curated S3 bucket, located in the 'aviris' folder, and is organized by date of the flight. Both the Zarr archives and the original raw data (in /raw) are located here.


Additional campaign raster pre-grid and vector data is available in the dh-shift-curated bucket in their respective folders.


Some example code for working with AVIRIS data is in the 'dh-shift-shared/notebook-template.ipynb' notebook. Additional examples are here: https://github.com/marinadunn/SHIFT-STAC-demo; specifically, take a look at this `notebook`_.

    .. _notebook: https://github.com/dieumynguyen/SHIFT-STAC-demo/blob/main/data_visualization_demo.ipynb

Streamlined Xarray Interface to AVIRIS Datasets
===============================================

We have an experimental capability to access the entire set of AVIRIS gridded mosaics as a single Xarray dataset (that can be subset by space, time, and wavelength). To open the dataset, code like the following (pay careful attention to the open_dataset arguments, position of brackets, quotes, etc.)

::

    import xarray as xr

    dat = xr.open_dataset("reference://", engine="zarr", backend_kwargs={
        "consolidated": False,
        "storage_options": {"fo": "s3://dh-shift-curated/aviris/v1/gridded/zarr.json"}
    })

    #From there, you can do things like:

    # Select a pixel at a time step
    dsub = dat.sel(x=750_000, y=3_830_000, time="2022-02-24", method="nearest")

    # Extract a time series for a pixel
    dsub = dat.sel(x=750_000, y=3_830_000, method="nearest")

    # Select multiple adjacent pixels at a particular time
    dsub = dat.sel(x=750_000, time="2022-02-24", method="nearest").drop("x").sel(y=slice(3_830_020, 3_830_000))

    # Calculate a vegetation index through time
    dsub = dat.sel(x=750_000, y=3_830_000, method="nearest")
    red = dsub.sel(wavelength=660, method="nearest").reflectance
    nir = dsub.sel(wavelength=800, method="nearest").reflectance
    ndvi = (nir - red) / (nir + red)

Additional examples are provided in the 's3://dh-shift-shared/example-read-aviris-zarr.ipynb' notebook.

