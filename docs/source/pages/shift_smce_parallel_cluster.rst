==========================
SHIFT SMCE Parallel Cluster
==========================

Getting Access
==============
In order to get access a request must be submitted to the SMCE admin team after
creating an ssh key pair, reviewing the SMCE training materials, and signing the user agreement

1. Read through the following training documents.

    * :download:`2022 SMCE_Elevated Privileges Security Training <../pdfs/2022_SMCE_Elevated_Privileges_Security_Training.pdf>`

    * :download:`2022 SMCE General Security Training <../pdfs/2022_SMCE_General_Security_Training.pdf>`

2. Sign the SMCE User Agreement.

    * :download:`2022 SMCE User Agreement <../pdfs/2022_SMCE_User_Agreement.pdf>`



3. Open a terminal and create a ssh key pair (public and private) with:

::

    ssh-keygen

4. Email smce-admin@lists.nasa.gov, and attach the public key **NOT PRIVATE**
(your public key should have a .pub extension and your private key should be a text file)
and your signed user agreement.

5. An administrator will contact you when you have been grated access to the system.

Connecting and Logging In
=========================


Command Line Access
-------------------
To access the cluster from the command line open up a fresh terminal and use the following command.

::

    ssh -i <path-to-private-key> <user-name>@XX.XXX.XX.XXX

Putty and WinSCP (Recommended)
------------------------------

Putty
^^^^^

Putty is an open-source terminal emulator, serial console and network file transfer application that
can be found in the NASA OCIO Software Center.

1. Once Putty has been downloaded, open PuttyGen

.. image:: ../images/puttygen.jpg
    :scale: 60%

|

2. Click load and find your private key .txt file (set the file type to all files)

.. image:: ../images/all_files.jpg
    :scale: 60%

|

3. Save the private key (do not overwrite your txt file)

4. Open up Putty

.. image:: ../images/putty_interface.jpg
    :scale: 60%

|

5. Enter in your user and host name (1) (username@xx.xxx.xx.xxx).

6. Using the navigation bar go to SSH and click on Auth.

7. Find the secret key you created with PuttyGen.

8. Return to Session using the navigation bar.

9. Enter a save name in the saved sessions area and click save (2).

10. Click the saved session (2).

11. Click load and then open.

WinSCP
^^^^^^

WinSCP is a popular SFTP and FTB client for Windows and can be used to easily transfer
files from your local machine to the server. WinSCP can be found in the NASA OCIO Software Center.

1. Open WinSCP

.. image:: ../images/win_scp_interface.jpg
    :scale: 60%

|

2. Input host name, user name and port 22, similar to Putty

3. Go to Advanced -> Advanced -> SSH-> Authentication

.. image:: ../images/win_scp_interface_advanced.jpg
    :scale: 60%

|

.. image:: ../images/win_scp_interface_advanced_key.jpg
    :scale: 60%

|

4. Load the key you created with PuttyGen and click ok.

5. Save the profile you created (not with password).

6. Select the saved profile and log in.


Storage Options
===============
home directory

Submitting Jobs
===============

https://slurm.schedmd.com/tutorials.html

Managing Environments
=====================

In order to start up a conda environment open .bashrc using a text editor. Copy and paste
the following code at the bottom of the file and save. Log out and back in and the conda
base environment should start.

::

    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('/data/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
    else
        if [ -f "/data/miniconda3/etc/profile.d/conda.sh" ]; then
            . "/data/miniconda3/etc/profile.d/conda.sh"
        else
            export PATH="/data/miniconda3/bin:$PATH"
        fi
    fi
    unset __conda_setup

    if [ -f "/data/miniconda3/etc/profile.d/mamba.sh" ]; then
        . "/data/miniconda3/etc/profile.d/mamba.sh"
    fi
    # <<< conda initialize <<<


**Note: Make sure to create your own environment and activate it before
downloading any Python packages.**

See :ref:`venv` to create your own Conda environment.

|