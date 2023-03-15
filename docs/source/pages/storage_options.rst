===============
Storage Options
===============

Users currently have the following storage options:

Home directory
--------------

    Appears as `/` in the file browser; full path is `/home/jovyan`.
    This is regular file-system storage. It is private to your user, but is limited in terms of space (10GB),
    so use this sparingly. It is persistent across sessions,
    but we recommend making sure all important files are backed up.



EFS
---

    Appears as `efs` in the file browser (relative to the home directory); full path is `/home/jovyan/efs`.
    This is regular file-system storage. This is shared across all users,
    but if you use this, you are strongly recommended to create user and/or sub-project-specific
    subdirectories here to keep things organized. This is technically unlimited,
    but is on a pay-for-what-you-use model, so please use responsibly.
    It is more expensive and, usually, somewhat less performant than S3.

.. _permissions:

Permissions
^^^^^^^^^^^

    The default permission are 755 and 644 meaning the owner can read/write/execute. The group and others can only
    read and execute, but not write. However, if you plan on accessing EFS storage from a different system, such as the SHIFT cluster, and would like to write to the
    EFS directories/files you created on Daskhub or vice versa the permissions for each directory/file will need to be updated.


    A combination of the following two commands can be used to change directory/file permissions:

    #. Using :code:`chmod 775` for directories or :code:`chmod 664` for files (owner read/write/execute, group read/write/execute, others read/execute) on the system where the directory/file was created will change the permissions so they it accessible
       from both. **Chmod is used to update permissions for directories or files that have already been created.** The command needs to be used to change the permissions for each directory (including -R will update all files in the
       directory) or for each individual file you would like to access from both systems.

    #. Using the umask command you can change the default permissions set for each directory or file **upon creation**.
       running :code:`umask 002` will give you the same permissions as chmod 775/664. This command will have to be run each time you
       log in. To make this change permanent, add the command to your .bashrc file in your
       root directory and it will automatically run everytime you log in. **This has to be done on both the cluster, Daskhub or any system accessing EFS storage.**
       This command will not update the permissions for files/directories that have already been created.

.. _s3_buckets:

S3 buckets
----------

    Appears in the bucket browser, not the file browser. These are object-based stores,
    not file system stores, so they are accessed somewhat differently, especially from code. Like EFS,
    these are “pay-for-what-you-use”. See “Working with datasets” below. There are 3 buckets that you should work on:

    **These buckets are mounted, but are technically READ ONLY. Do not attempt to write to them or they
    will crash.**

    * dh-shift-curated

            This is where processed and organized datasets from the SHIFT campaign are located.
            Technically, you can write to this S3 bucket, but please treat it as effectively read only unless you are
            producing a product that you are prepared to share. This storage is fully publicly available.
            Please see additional details on accessing these datasets below.

    * dh-shift-shared

        This should be used for data shared across all SHIFT data system users,
        but not publicly available. Please use “folders” inside this bucket to help with organization.

    * dh-shift-users

        This should be used for “private” user storage. Eventually, users will only be able to see their own
        folders here; however, we’re still figuring out how to do that, so this currently works the same as
        `dh-shift-shared`, so you shouldn’t store anything private in here. Before using this, please create a
        “folder” with your username in the root directory, to help with organization.

    * NOTE 1:

        Jupyter notebooks natively support editing and execution from inside S3 buckets.
        There isn’t a one-click button for creating a notebook in S3, so the workflow is to take an
        existing blank notebook, copy it, and then work from the copy. For specific instructions,
        take a look at `/dh-shift-shared/notebook-template.ipynb` (which you can find in the S3 browser).

    * NOTE 2:

        EFS and S3 buckets have effectively unlimited storage, but are on a “pay-for-what-you-use” model.
        That means that SBG is charged per GB-hour of storage on these devices: Storing 1 GB of data for 1 hour costs
        the same as storing 500 MB of data for 2 hours or 2 GB of data for 30 minutes, and so on. At the expected scale
        of this project, this is not that expensive, we have plenty of funds, and we are actively monitoring costs,
        so don’t be afraid to use what you need! But, please be responsible — don’t store large amounts of data
        (100s of GB) in these services for long periods of time unless you need to for your work; avoid creating
        unnecessary copies of large data; etc