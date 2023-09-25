Running ISOFIT on the SHIFT Cluster
===================================

Getting access to the cluster
-----------------------------

The first step is getting access to the cluster. See the `SHIFT SMCE Parallel Cluster <https://shift-smce-user-guide.readthedocs.io/en/latest/pages/shift_smce_parallel_cluster.html>`_ page.


Setting up ISOFIT
-----------------

Cloning the ISOFIT Repository
+++++++++++++++++++++++++++++
The first step is to clone the `ISOFIT Github repository <https://github.com/isofit/isofit>`_. You can clone ISOFIT to your root directory or create a directory on EFS using your username as the directory 
name. There is a copy of the repository available on the EFS drive however, I recommend cloning your own copy if you plan on running the examples.

If you plan on accessing your EFS directory from both the cluster and the Daskhub, you will need to adjust the permissions for the directory you created. **Read the information about directory and file** :ref:`permissions` **if you plan on using EFS storage**.

ISOFIT Emulators
++++++++++++++++
The SRTMnet and 6S models can be found on the efs drive and are ready for use

ISOFIT Conda Environment
++++++++++++++++++++++++

The SHIFT cluster already has a Conda environment set up named ans_isofit. Feel free to use this environment, however please do not install additional packages as this could cause dependency issues.

Running the Small Image Cube Example
------------------------------------
 
Navigate to the image cube example (isofit/example/image_cube). Using your favorite text editor (vim, nano, etc) create the following script:

::

    #!/bin/bash
    #SBATCH --partition shift-c5n4xlarge-spot
    #SBATCH --job-name small_image_cube

    source /data/miniconda3/etc/profile.d/conda.sh
    conda activate ans_isofit
    ./run_small.sh

This simple script will start up the isofit conda environment and run the example on the SMCE cluster using SLURM. Before running, The configuration file and run_small script need to be updated.

* Config File:
    Change the emulator path to "/efs/sRTMnet/sRTMnet_v100"

* run_small script:
    isofit base path must be changed to the location of your gitrepo e.g. "/efs/<your_efs_dir>/isofit/isofit"


Running ISOFIT
--------------

To submit a job to the cluster via Slurm, use the following command:

::

    sbatch <name_of_slurm_script> or srun <name_of_slurm_script>


Once The job has been submitted you can view the cluster queue and watch progress using the following:

::

    watch squeue



Troubleshooting
---------------

Some common issues that cause ISOFIT to fail:

* Incorrect file paths

    Double check all file paths to make sure they are formatted correctly. Make sure if you are using relative filepaths, they are formated correctly.


* File permissions

    **Read the information about directory and file** :ref:`permissions`.


* Incorrect file types (Input data must be in the ENVI binary format). Here a simple example for converting :download:`NetCDF files to ENVI  <../resources/netcdf_to_envi.py>`.


* Delete all outputs before re-running.