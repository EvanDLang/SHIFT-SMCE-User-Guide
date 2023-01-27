.. _use_slurm_doc:

Using SLURM to Submit Jobs
--------------------------

For management and monitoring of the
computational workload on Svante,  we use the commonly implemented `SLURM <https://slurm.schedmd.com>`_
(Simple Linux Utility for Resource Management) software.
Users submit jobs through this resource management system, which places jobs in a queue
until the system is ready to run them. SLURM selects which jobs to run, when and where, according to a pre-determined
policy meant to balance competing user needs and to maximize efficient use of cluster resources. Note that one
cannot ``ssh`` to a compute node unless one has a job running on that node via the queue system, so users have no alternative
but to use SLURM for access to compute nodes.

This is meant to be a quick and dirty guide to get one started, although in reality it is probably
as detailed as an average user might ever require. To use SLURM, create a batch job command
file for submission on a terminal command line. A batch job file is simply a shell script containing
a set of commands specifying to run on some set of cluster compute nodes. It also contains directives
that specify job attributes and resource requirements that the job needs (e.g. number of compute nodes, runtime,
hardware type etc.) SLURM-directed statements in this script have the syntax ``#SBATCH «directive»``, with
several common directives given in the example below (in a shell script, note that all other lines starting with ``#`` are ignored as comments,
except for the shell type specification line at the top, e.g., ``#!/bin/bash`` ).

Similar to the module system,
there is an abundance of SLURM documentation available on the web, but note the syntax in SLURM varies by version
(currently, using `SLURM 22.05.2 <https://slurm.schedmd.com/archive/slurm-22.05.2/>`_ ) so what you find
on the web might not exactly match our SLURM implementation.

.. _slurm_simple_ex:

SLURM batch script example
**************************

::

   #!/bin/bash
   #
   # filename: slurm_script
   #
   # Example SLURM script to run a job on the svante cluster.
   # The lines beginning #SBATCH set various queuing parameters.
   #
   # Set name of submitted job

   #SBATCH -J example_run

   #
   # Ask for 3 cores

   #SBATCH -n 3

   #
   # Submit with maximum 24 hour walltime HH:MM:SS

   #SBATCH -t 24:00:00

   #
   echo 'Your job is running on node(s):'
   echo $SLURM_JOB_NODELIST
   echo 'Cores per node:'
   echo $SLURM_TASKS_PER_NODE


A complete list of shell environment variables set by SLURM is available in online documentation;
from a terminal window, type ``man sbatch``.

Note many ``#SBATCH`` statement options have a single dash and letter, followed by the argument.
There is an equivalent “long-form” syntax using a double dash and equals sign,
i.e. ``-n 3`` is the same as ``--ntasks=3``. Some  options only exist via the long-form syntax.
Also, fair warning, SLURM terminology lazily uses the term ‘cpu’ when it really means ‘core’;
these are not the same, as a cpu is a physical chip that has anywhere from 1 to 32 cores on it
(and all svante compute nodes are dual-cpu aka dual-socket); each core can run a single process or thread.

.. _slurm_basic_options:

Common ``#SBATCH`` options
**************************

The following is a list of the most useful ``#SBATCH`` options:

``-n`` (``--ntasks=``) requests a specific number of cores; each core can run a separate process.

``-N`` (``--nodes=``) requests a specific number of nodes. If two numbers are provided, separated by a dash,
it is taken as a minimum and maximum number of nodes. If impossible to fit your job on N nodes (i.e. when used in tandem with options such as –n), more nodes may be allocated.

``--ntasks-per-node=`` specifically ask for this number of cores on each node requested (thus, typically used in conjunction with ``–N``).

``-p`` (``--partition=``) requests nodes from a specific partition. Our partitions are set up as FDR and EDR based on compute nodes’ IB type (see :numref:`svante_nodes`).
One can list both partitions separated by a comma – but note that SLURM cannot mix cores across partions for a single ``–n xx`` request
(as MPI jobs cannot span different partitions). If you don’t specify a partition, the “node hunting order” is FDR first, then EDR.

``-t`` (``--time=``) requests a specific (wall-) time allocation for your job: if your job has not completed by the end of this time, it is killed.
Try to estimate how long your job will run, then add some number of hours as padding in case it runs a bit slower than expected.
It is important to the scheduler that this time is reasonably accurate, because if jobs are backed up the scheduler must decide which new jobs to run first,
and will use this info to make decisions. The scheduler assumes all running jobs will use their full walltime allocation.
If jobs are backed up, your job might start sooner with a shorter time request. Acceptable time formats include
``«minutes»``, ``«minutes»:«seconds»``, ``«hours»:«minutes»:«seconds»``, ``«days»-«hours»``,
``«days»-«hours»:«minutes»`` or ``«days»-«hours»:«minutes»:«seconds»``.

``-J`` (``--job-name=``) your job will show up under this name when you ask for a list of running jobs
(``squeue`` command, see below). Very helpful if you want to keep track of your individual jobs’ status
if you have several submitted simultaneously.

``--mem-per-cpu=`` requests a certain amount of RAM available for each core. Useful for parallel (MPI or openMP)
jobs where you know each core has a specific RAM requirement. Can also be useful for single-threaded jobs especially if you
have a large RAM requirement (e.g. optimization applications). Unit is MB; in other words,  ``mem-per-cpu=8000``
would request 8000MB (=8GB) but one can also specify as ``--mem-per-cpu=8G``. Svante default is 4GB.

``--mem=`` requests a certain amount of (total) RAM per node to be used. Note the special case ``--mem=0`` which requests ALL the available RAM on each node requested.
**Warning:** this option removes some system safeguards, be careful to not use more RAM than available on the node.

``-w`` (``--nodelist=``) use this option if you need to specify particular compute nodes on which to run.
Multiple nodes can be separated with commas or specified as a list such as ``c[072-075]``
(if using C shell, you will need to put quotes around this shorthand to specify a list of nodes, but quotes not needed using bash).
This option can work in conjunction with ``–n`` or ``--ntasks_per_node``.

``--exclude=`` is used to exclude nodes from running your job. This might be useful, say,
if you wanted to run exclusively on stooge nodes, you could exclude c041-c060 from the FDR partition.

``-a`` (``--array=``) is used to submit an ensemble of single-threaded jobs, a fairly common task in the Joint Program.
An example of an array batch script is given :ref:`below <slurm_array_example>`.

A few additional comments:

-  multiple options can be combined on a single ``#SBATCH`` line, e.g. ``#SBATCH -n 32 -p edr`` .

-  SLURM includes "resource protection" of users' RAM and cores once they are allocated to a specific job.
   Most applications are pretty good about sharing resources, but others, such as MATLAB, are resource hogs. For MATLAB,
   it is better to request a single node (preferably, a FDR node) and use the ``--mem=0`` option;
   as such, you have exclusive access to the compute node for the duration of the job.

-	There are many more available SLURM options as listed via ``man sbatch``. Ask for help if there is something in particular you require for your script.

How to submit a SLURM job
*************************

The SLURM ``sbatch «slurm_script_filename»`` command is used to submit job script files for scheduling and execution. For example:

::

  $ sbatch «slurm_script_filename»
  Submitted batch job 16218

Notice that upon successful submission of a job, SLURM returns a job identifier, an integer number assigned by SLURM to that job (here, jobid=16218).
You'll see your job identified by this number, and will need this id for specific actions involving the job, such as canceling the job.
Your job will run in the current directory from where you submit the ``sbatch`` command
(although you can direct it elsewhere in the script, using a ``cd`` command).
After submitting a slurm job script, upon completion one should get an output file ``slurm-«jobid».out``
(this filename can be changed via a ``#SBATCH –o`` option). Output from the example script :ref:`above <slurm_simple_ex>` might contain:

::

  Your job is running on node(s):
  c043
  Cores per node:
  3

In this output, you were assigned 3 cores on a single FDR node, ``c043``.

Some useful terminal window commands to monitor Svante's load:

``squeue`` - list both active and pending jobs submitted to SLURM, providing various info about the jobs, including
expected start time if the job is pending. ``squeue -u «username»`` wil limit output to your jobs only.

``sinfo``  - shows the status of all nodes in the cluster.

``scontrol show node «nodename»``  - gives a full status report for «nodename» (if you leave off the nodename argument, it provides info for ALL nodes).

``scontrol show job «jobid»``  - gives a complete summary of settings for a running (or pending) job «jobid». Once the job is complete, ``seff «jobid»`` will
provide infomation about the job, including CPU and memory use and efficiency.

``scancel «jobid»`` - immediately kills the job with «jobid» whether queued up or running (useful for a job submitted in error, or job not running as desired etc.)

Note that all nodes in the cluster (i.e. file servers, login node) have slurm installed and will respond to above commands, job submissions etc.
Typically however we recommend submitting slurm jobs from ``svante-login``.
[2022 status: slurm capabilities not yet active on all file servers]

Requesting resources for multi-core, multi-node jobs
****************************************************

There is no single right or 'best' way to request resources across nodes and cores; it depends
on the size and details of your job, whether you are running MPI or shared memory (openMP), among other considerations.
Some examples and suggestions are as follows.

``#SBATCH –n 48 –p edr`` is a recommended way to request 48 cores (here, requesting EDR nodes) for a modestly sized MPI job.
There is no constraint whether one gets for example 32 on one node and 16 on another, or alternatively 8 cores on six separate nodes;
the scheduler will determine this. For an MPI job sufficiently large to span several compute nodes, usually one does not care how the cores are distributed.

``#SBATCH –N 2 –n 16`` would cause the scheduler to find 16 free cores spread across two nodes;
it might give you 15 on one machine and 1 one the second, which might not be desired. Alternatively,
``#SBATCH –N 2 –-ntasks-per-node=8``  would get you 8 cores on both nodes.
Certainly, if you need a large number of nodes for a large MPI job, there is no harm to specifying the
breakdown into N nodes of ntasks-per-node cores instead of simply using the –n spec
(the exception would be during heavy cluster usage, the scheduler might be able to fill a more general –n request more quickly).

``#SBATCH –N 1 –n 32`` would request a single node with 32 cores. At present, only EDR or HDR nodes would fulfill this request, as all FDR nodes
contain fewer than 32 cores. If you are running a shared-memory/openMP application such as `GEOS-Chem Classic <http://acmg.seas.harvard.edu/geos/>`_
this would allow for 32 parallel cores on a single node (openMP jobs cannot span across multiple nodes). If you requested  ``-n 16``, or 16 cores,
your job might run on either FDR, EDR or HDR nodes, whatever was available; in fact, the scheduler might
allocate two ``#SBATCH -N 1 -n 16`` jobs on a single EDR node.

As mentioned, one might want to “take over a full compute node”, including use of all memory, which can be accomplished for example:
``#SBATCH –N 1 –n 16 –-mem=0 –p fdr``, requesting 16 cores on a FDR node. Generally, request a machine with just the number of cores or total RAM you require.
No other users’ jobs can be assigned to this node, because any additional job assignment would require available RAM.
This might be useful to run large or parallel-enabled MATLAB or Python scripts, for example.

.. _slurm_interactive:

Interactive SLURM sessions
**************************

SLURM also provides a special kind of batch job called interactive-batch. An interactive-batch job is treated just like a regular batch job,
in that it is placed into the queue system and must wait for resources to become available before it can run. Once it is started,
however, the user's terminal input and output are connected to the job in what appears to be a ``ssh`` session on one of the compute nodes.
In other words, this is how one can get on a compute node to do analysis or run jobs without the formal requirement of a SLURM/sbatch script.
For example, to obtain a bash shell on a FDR node, a single core job:

::

  $ srun --pty -p fdr -n 1 /bin/bash
  bash-4.3$ hostname
  curly
  bash-4.3$ echo $SLURM_NPROCS
  1

In this example the user was assigned one core on node ``curly``.
(Note: legacy C shell users, replace the last argument in the ``srun`` command with ``/bin/tcsh``.)

Once you start the interactive job, you are automatically logged into the node allocated by SLURM.
If you request multiple nodes, you are logged into the first in the list of assigned nodes/cores.
Type exit from this shell to end the interactive session. To use X-window forwarding in an
interactive session, add option ``–-x11=first`` to the ``srun`` command. Fair warning however,
X-window forwarding can make for a slow user interface, see :ref:`svante-ood <svante_ood>` as a possible faster alternative.

Further SLURM script examples
*****************************

A fairly straightforward MPI job is shown below, a run of MITgcm.
The script requests 48 cores on EDR compute nodes (MITgcm is very sensitive to IB speed,
so it runs noticeably faster on EDR or HDR nodes), without specifying how these cores are allocated across nodes.
Modules ``intel/2017.0.1`` and ``openmpi/1.10.5`` are loaded;
specifying the module version at load time, as done here, is good general practice which saves aggravation if not
specified and the default is changed, causing your code to crash.
See :numref:`modules_doc` for explanation of the ``source`` command proceeding the module load statements.
When the script is submitted, it won't be known which node(s) the scheduler will allocate.
Notice the script is also asking for 6G RAM per core,
perhaps the model setup here employs a large grid, albeit for most setups this spec is not necessary as the 4G default is usually sufficient.
As such, however, the scheduler will NOT assign a full 32 cores on a single EDR node, as 32*6 = 192GB > 128GB available on each node (see :numref:`svante_nodes`).

::

   #!/bin/bash
   #
   #SBATCH -J MITgcm_exp1
   #SBATCH –n 48
   #SBATCH –p edr
   #SBATCH –t 2-12:00:00  # format is DAYS-HOURS:MINUTES:SECONDS
   #SBATCH --mem_per_cpu=6G

   source /etc/profile.d/modules.sh
   module load intel/2017.0.1
   module load openmpi/1.10.5

   OEXEDIR=/home/jscott/MITgcm/ocn_build

   echo 'Your job is running on node(s):'
   echo $SLURM_JOB_NODELIST
   echo 'Cores per node:'
   echo $SLURM_TASKS_PER_NODE
   module list

   mpirun -V –v -np 48 $OEXEDIR/mitgcmuv > std_outp

   exit 0


The ``mpirun`` command above will by default use the infiniband pathway for MPI communication.
(For reference, the default syntax is equivalent to ``mpirun`` with option   ``--mca btl openib,sm,self`` ;
alternatively, ``--mca btl tcp,sm,self`` would select ethernet communication for MPI.)

Given that all our compute nodes are Intel-based, the Intel fortran compiler is able to produce a significantly faster executable than PGI or gcc.
We strongly encourage folks to make the effort to compile with Intel; moreover, the long-term future of PGI’s parent company is unclear, and for the time being
we have stopped updating new PGI versions.

.. _slurm_array_example:

Finally, an example that uses special syntax for an array job (``#SBATCH –a`` option) for doing a large ensemble of single-processor runs:

::

   #!/bin/bash
   #SBATCH -J ensemble_100
   #SBATCH -n 1
   #SBATCH -t 2:00:00
   #SBATCH -a 1-100%20

   echo $SLURM_JOB_NODELIST

   ./prog.exe  > outfile$SLURM_ARRAY_TASK_ID


This script will run ``prog.exe`` (in the local directory) 100 times, producing 100 output files named ``outfilexxx`` where xxx will be 1-100
(making use of SLURM environment variable ``SLURM_ARRAY_TASK_ID``).
You will also get 100 SLURM output files ``slurm-«jobid»_xxx.out`` which will contain output of ``echo $SLURM_NODELIST``.
The (optional) additional specification ``%20`` means that only 20 jobs will run simultaneously, effectively limiting your
usage “footprint” on the cluster. This might be important if you had an even larger ensemble to run;
if you don’t specify the % option your jobs mightly completely fill the cluster until done, making it difficult
for anyone else to get new runs started (note that no partition request is specified; these jobs will
run on any free nodes). One probably would also want to modify this script so that each run receives different input parameters.
The nice thing here is that the scheduler handles finding nodes for you in a system-friendly fashion.
An equivalent, but ugly, brute force approach would be to simply loop through a ``sbatch`` command 100 times in a shell script.