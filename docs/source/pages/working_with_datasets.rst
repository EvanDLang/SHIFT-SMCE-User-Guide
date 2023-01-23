=====================
Working With Datasets
=====================

.. container:: cell markdown
   :name: f86e674a-0fe8-4733-b08e-e6049972a326

   All of the SHIFT AVIRIS-NG data lives in the dh-shift-curated S3
   bucket, located in the ‘aviris’ folder, and is organized by date of
   the flight. Both the Zarr archives and the original raw data (in
   /raw) are located here.

.. container:: cell markdown
   :name: d028d87c-6cc3-41c7-8596-20b908c72721

   Additional campaign raster pre-grid and vector data is available in
   the dh-shift-curated bucket in their respective folders.

.. container:: cell markdown
   :name: 2ecda34d-d623-48aa-8a00-9ac03c5ffa12

   Some example code for working with AVIRIS data is in the
   ‘dh-shift-shared/notebook-template.ipynb’ notebook. Additional
   examples are here: https://github.com/marinadunn/SHIFT-STAC-demo;
   specifically, take a look at this
   `notebook <https://github.com/dieumynguyen/SHIFT-STAC-demo/blob/main/data_visualization_demo.ipynb>`__.

Streamlined Xarray Interface to AVIRIS Datasets
===============================================

.. container:: cell markdown
   :name: f7100684-02f3-4e97-8037-dd893d4a399e

   We have an experimental capability to access the entire set of AVIRIS
   gridded mosaics as a single Xarray dataset (that can be subset by
   space, time, and wavelength). To open the dataset, code like the
   following (pay careful attention to the open_dataset arguments,
   position of brackets, quotes, etc.)

.. container:: cell code
   :name: 3b5eb83b-537a-4730-8e60-3b3eac819244

   .. code:: python

      import xarray as xr
      import matplotlib.pyplot as plt

      dat = xr.open_dataset("reference://", engine="zarr", backend_kwargs={
          "consolidated": False,
          "storage_options": {"fo": "s3://dh-shift-curated/aviris/v1/gridded/zarr.json"}
      })

.. container:: cell code
   :name: 141ab9c7-e9ce-474d-80a7-c73fa86cfe83

   .. code:: python

      # Select a pixel at a time step and plot the reflectance
      dsub = dat.sel(x=750_000, y=3_830_000, time="2022-02-24", method="nearest")
      dsub.reflectance.plot()


   .. container:: output display_data

      .. image:: ../images/working_with_datasets_cell_7_output_1.png

.. container:: cell code
   :name: 70923059-18b1-4140-aa66-337d11977644

   .. code:: python

      # Extract a time series for a pixel
      dsub = dat.sel(x=750_000, y=3_830_000, method="nearest")
      dsub.dims

   .. container:: output execute_result

      ::

         Frozen({'time': 13, 'wavelength': 425})

.. container:: cell code
   :name: 036e45cd-a357-42ed-b708-bb449f538c30

   .. code:: python

      # Select multiple adjacent pixels at a particular time
      dsub = dat.sel(x=750_000, time="2022-02-24", method="nearest").drop("x").sel(y=slice(3_830_020, 3_830_000))
      dsub.dims

   .. container:: output execute_result

      ::

         Frozen({'y': 4, 'wavelength': 425})

.. container:: cell code
   :name: 1309e82a-8c02-48eb-9a75-1a3b959e0445

   .. code:: python

      # Calculate a vegetation index through time for a pixel
      dsub = dat.sel(x=750_000, y=3_830_000, method="nearest")
      dsub.dims
      red = dsub.sel(wavelength=660, method="nearest").reflectance
      nir = dsub.sel(wavelength=800, method="nearest").reflectance
      ndvi = (nir - red) / (nir + red)
      ndvi.plot()
      plt.ylabel("NDVI")
      plt.draw()

   .. container:: output display_data

      .. image:: ../images/working_with_datasets_cell_10_output_0.png
