Working With Other Data On SHIFT SMCE
=====================================

EMIT Data
---------

The EMIT team has put together a thorough set of tutorials on how to access and work with the data on `github`_. The easiest way to work with the EMIT data is by using direct s3 access (see the link below).

    .. _github: https://github.com/nasa/EMIT-Data-Resources


- To set up a work environment use the following script to get `direct access the LP DAAC data pool with Python <https://github.com/nasa/EMIT-Data-Resources/blob/main/setup/EarthdataLoginSetup.py>`_. There is no need to setup the emit conda environment as the default conda environment (notebook) should have all the packages required for working with the data.

- `Getting for EMIT data via EarthData search <https://github.com/nasa/EMIT-Data-Resources/blob/main/guides/Getting_EMIT_Data_using_EarthData_Search.md>`_


- `Direct s3 access for EMIT Data <https://github.com/nasa/EMIT-Data::-Resources/blob/main/how-tos/How_to_Direct_S3_Access.ipynbL>`_


- `Extracting and area from EMIT imagery <https://github.com/nasa/EMIT-Data-Resources/blob/main/how-tos/How_to_Extract_Area.ipynbL>`_



Harmonized Landsat Sentinel-2
------------------------------

- Follow the first step under EMIT data to get `direct access the LP DAAC data pool with Python <https://github.com/nasa/EMIT-Data-Resources/blob/main/setup/EarthdataLoginSetup.py>`_.

- Use `EarthData search <https://search.earthdata.nasa.gov/search>`_ to find data.

.. image:: ../images/earthdata_search_example.png

The following code shows how to get direct s3 access.

::

    import requests
    import s3fs
    import rasterio as rio
    import rioxarray as rxr
    
    s3_cred_endpoint = {
    'podaac':'https://archive.podaac.earthdata.nasa.gov/s3credentials',
    'gesdisc': 'https://data.gesdisc.earthdata.nasa.gov/s3credentials',
    'lpdaac':'https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials',
    'ornldaac': 'https://data.ornldaac.earthdata.nasa.gov/s3credentials',
    'ghrcdaac': 'https://data.ghrc.earthdata.nasa.gov/s3credentials'
    }
    
        
    def get_temp_creds(provider):
        return requests.get(s3_cred_endpoint[provider]).json()
    

Get Credentials

::

    temp_creds_req = get_temp_creds('lpdaac')

Pass Authentication to s3fs

::

    fs_s3 = s3fs.S3FileSystem(anon=False, 
                              key=temp_creds_req['accessKeyId'], 
                              secret=temp_creds_req['secretAccessKey'], 
                              token=temp_creds_req['sessionToken'])
                          
::

Access the data using rasterio or rioxarray

::

    s3_url = "s3://lp-prod-protected/HLSL30.020/HLS.L30.T56JKT.2023078T235959.v2.0/HLS.L30.T56JKT.2023078T235959.v2.0.B01.tif"
    
    ds = rxr.open_rasterio(s3_url)
    
    with rio.open(s3_url) as src:
        print(src.profile)