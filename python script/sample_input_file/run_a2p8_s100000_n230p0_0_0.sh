#!/bin/bash
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH -o a2p8_s100000_n230p0_0_0.out
#SBATCH -e a2p8_s100000_n230p0_0_0.err
#SBATCH -p randleslab-ib

export I_MPI_OFI_LIBRARY_INTERNAL=0

source /opt/apps/rhel8/intel-2020/compilers_and_libraries/linux/bin/compilervars.sh intel64
export LD_LIBRARY_PATH=/opt/apps/staging/libfabric-1.15.1-rhel8/lib:/usr/lib64:/usr/lib64/libibverbs:/opt/apps/rhel7/compatlib:$LD_LIBRARY_PATH

export I_MPI_FABRICS=shm:ofi
export FI_PROVIDER=verbs

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

export I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS="--cpu-bind=none"
export I_MPI_HYDRA_BOOTSTRAP=slurm
export I_MPI_HYDRA_BOOTSTRAP_EXEC=srun

echo "------------------------------------------------------------------------------"
mpirun -np 128 src/harvey.linux run/input_a2p8_s100000_n230p0_0_0.i
echo "------------------------------------------------------------------------------"
    