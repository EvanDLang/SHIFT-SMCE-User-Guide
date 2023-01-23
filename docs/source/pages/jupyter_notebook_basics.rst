=======================
Juypter Notebook Basics
=======================

Jupyter notebooks provide a literate interactive programming environment where you can mix code, code output (including static and interactive visualizations), and text (formatted as Markdown). There are a large number of tutorials on Jupyter notebooks online; here is `one interactive example`_, and here is the `JupyterLab-specific notebook interface justification`_.

    .. _one interactive example: https://mybinder.org/v2/gh/ipython/ipython-in-depth/HEAD?urlpath=tree/binder/Index.ipynb

    .. _JupyterLab-specific notebook interface justification: https://jupyterlab.readthedocs.io/en/stable/user/notebook.html


Kernels
=======

Jupyter notebooks work by running a specific kernel corresponding to a specific running process of a particular programming language. In SHIFT, by default, we have a Python kernel linked to the default conda environment. This kernel already has many of the Python libraries you will need to do data analysis, and we can expand this base environment to accommodate reasonable user requests.


In addition, you can create your own kernels which with new conda environments with specific Python packages.

You can change the kernel of any notebook by clicking the kernel name (default: "Python 3 (ipykernel)") in the top right corner of the notebook interface.

Setting Up a New Kernel
=======================
The process for setting up a kernel starts with configuring a new virtual environment.

Creating a New Conda Environment
================================
* Open a new terminal
* Deactivate the current Conda environment

::

    conda deactivate

* Create a new environment (choose one)

::

    #Create a Conda environment from the base environment
    conda create -n <your-env-name>

    #Create a Conda environment from an existing environment
    conda create --name <your-env-name> --clone <name-of-existing-environment>

    #Create a clean Conda environment
    conda create --name <your-env-name> python --no-default-package

* Activate your new environment and install ipykernel and other packages

::

    conda activate <your-env-name>
    pip install ipykernel

* Adding the new kernel

**Note:** Make sure your new Conda environment is active
::

    python -m ipykernel install --user --name=<kernel-name>



Kernel Management
=================

::

    #List existing kernels
    jupyter kernelspec list

    #Remove a Kernel
    jupyter kernelspec uninstall <kernel-name>


More information can be found in the `Conda`_  and `Jupyter Lab`_ documentation!

    .. _Conda: https://conda.io/projects/conda/en/latest/index.html
    .. _Jupyter Lab: https://jupyterlab.readthedocs.io/en/stable/index.html
