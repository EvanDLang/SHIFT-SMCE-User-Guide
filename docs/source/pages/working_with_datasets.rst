Working With Datasets
=====================

The SHIFT AVIRIS-NG data is located in several spots. The gridded Zarr data can be found in mounted S3 bucket dh-shift-curated, located in the 'aviris' folder. The L1 and L2a products can be found in efs/efs-data-curated. Both are organized by the date of the flight. Additional campaign raster pre-grid and vector data is available in the dh-shift-curated bucket in their respective folders.

This user guide has several example notebooks demonstrating how to work with AVIRIS data which cover: Xarray basics, raster operations (reprojection, clipping with shapefiles), data visualization and clustering. Additionally, on the 'dh-shift-shared' mounted S3 bucket there is a notebook template for getting started. 


.. toctree::
   :maxdepth: 2

   ../notebooks/xarray_basics
   ../notebooks/visualizing_data
   ../notebooks/raster_operations
   ../notebooks/clustering_examples
   

Additional examples can be found here: https://github.com/marinadunn/SHIFT-STAC-demo; specifically, take a look at this `notebook`_.

    .. _notebook: https://github.com/dieumynguyen/SHIFT-STAC-demo/blob/main/data_visualization_demo.ipynb