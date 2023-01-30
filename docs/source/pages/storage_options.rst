===============
Storage Options
===============

Users currently have the following storage options:

Home directory
--------------

    Appears as `/` in the file browser; full path is `/home/jovyan`. This is regular file-system storage. It is private to your user, but is limited in terms of space, so use this sparingly. It is technically persistent across sessions, but we are still fiddling with it under the hood so don’t store anything here you wouldn’t be too upset about suddenly losing.

EFS
---

    Appears as `efs` in the file browser (relative to the home directory); full path is `/home/jovyan/efs`. This is regular file-system storage. This is shared across all users, but if you use this, you are strongly recommended to create user and/or sub-project-specific subdirectories here to keep things organized. This is technically unlimited, but is on a pay-for-what-you-use model, so please use responsibly. It is more expensive and, usually, somewhat less performant than S3.

S3 buckets
----------

    Appears in the bucket browser, not the file browser. These are object-based stores, not file system stores, so they are accessed somewhat differently, especially from code. Like EFS, these are “pay-for-what-you-use”. See “Working with datasets” below. There are 3 buckets that you should work on:

    * dh-shift-curated

            This is where processed and organized datasets from the SHIFT campaign are located. Technically, you can write to this S3 bucket, but please treat it as effectively read only unless you are producing a product that you are prepared to share. This storage is fully publicly available. Please see additional details on accessing these datasets below.

    * dh-shift-shared

        This should be used for data shared across all SHIFT data system users, but not publicly available. Please use “folders” inside this bucket to help with organization.

    * dh-shift-users

        This should be used for “private” user storage. Eventually, users will only be able to see their own folders here; however, we’re still figuring out how to do that, so this currently works the same as `dh-shift-shared`, so you shouldn’t store anything private in here. Before using this, please create a “folder” with your username in the root directory, to help with organization.

    * NOTE 1:

        We are working on “mounting” these buckets as folders in the home directory, which will dramatically simplify the process of accessing them. But that’s not done yet — stay tuned!

    * NOTE 2:

        Jupyter notebooks natively support editing and execution from inside S3 buckets. There isn’t a one-click button for creating a notebook in S3, so the workflow is to take an existing blank notebook, copy it, and then work from the copy. For specific instructions, take a look at `/dh-shift-shared/notebook-template.ipynb` (which you can find in the S3 browser).

    * NOTE 3:

        EFS and S3 buckets have effectively unlimited storage, but are on a “pay-for-what-you-use” model. That means that SBG is charged per GB-hour of storage on these devices: Storing 1 GB of data for 1 hour costs the same as storing 500 MB of data for 2 hours or 2 GB of data for 30 minutes, and so on. At the expected scale of this project, this is not that expensive, we have plenty of funds, and we are actively monitoring costs, so don’t be afraid to use what you need! But, please be responsible — don’t store large amounts of data (100s of GB) in these services for long periods of time unless you need to for your work; avoid creating unnecessary copies of large data; etc