============
Known Issues
============

Partial Subsetting
==================

Partial subsetting of ENVI binary files (the default storage format for SHIFT mosaics) using common approaches ('spectral.io.envi' and 'xarray/rioxarray.open_dataset') is currently very slow. Below is a more technical description of the problem and some possible solutions, but for now, just note that we are aware of the problem and working on resolving it.


Technical Background
====================

Accessing files in S3 is based on HTTP APIs, not file system calls. For example, reading a full file uses an HTTP "GET" request, while writing uses an HTTP "PUT" request. Libraries for S3 access — including libraries for "natively" reading S3

Possible Solutions
==================

    #. Performing range-get requests "by hand" (as in `this StackOverflow answer`_). This requires you to manually

        .. _this StackOverflow answer: https://stackoverflow.com/questions/42677924/download-subset-of-file-from-s3-using-boto3

    #. Converting the ENVI binary files into a cloud-optimized format (most likely Zarr) that supports cloud-native random subsetting. (Technically, Zarr “cheats” by breaking up the data into a bunch of individual chunks first, so you can retrieve a “subset” by just retrieving files corresponding to specific chunks).
