"""
generate input file for HARVEY, 2017
Junyu Nan,
Jun 9, 2022,
input: Axes, Stiffness, Gridspacing
Output: Plinkos_cell_size_stiffness.i
        celltype_ctc_size_stiffness.i
        runscript_cell_size_stiffness.i
Private use for generate input file for simulating CTCs
traveling though Plinko's geometry.
Current version allows change of cell axes and stiffness,
parameter change on grid spacing is allowed
"""

import numpy as np


def axes_to_str(axes):
    temp = str(axes)
    axes_str = ''
    for element in temp:
        if element == '.':
            element = 'p'
        axes_str += element
    return axes_str


def coord_to_str(coord):
    coord_str = ''
    x = 0
    for i in coord:
        if i > 0:
            float_part = i%1
            int_part = i - float_part
            coord_str += (str(int_part) + 'p' + str(float_part))
        if i == 0:
            coord_str += '0'
        if i < 0:
            i = -i
            float_part = i%1
            int_part = i - float_part
            coord_str += ('n' + str(int_part) + 'p' + str(float_part))
        if x < 2:
            coord_str += '_'
        x += 1
    return coord_str


def generate_file_name(axes, stiffness, coord_str):
    """generate the input file needed to run HARVEY
    input:
        list of float, axes
        list of int, stiffness
    output:
        list of string, file name"""
    axes_str = axes_to_str(axes)
    input_all = "input_a{}_s{}_{}.i".format(axes_str, stiffness, coord_str)
    input_cell = "celltype_ctc_a{}_s{}.i".format(axes_str, stiffness)
    runscript = "run_a{}_s{}_{}.sh".format(axes_str, stiffness, coord_str)
    cellcoord = "cellcoords_{}.i".format(coord_str)
    return [input_all, input_cell, runscript, cellcoord]


def input_all_content(file_name, axes, stiffness, grid, coord_str):
    input_all = open("run/" + file_name, "w")
    # write title of the file
    input_all.write(
    """
# # # # # # # # input file for new HARVEY # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Version: September 2017  # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # grid setup parameters # # # # # # # # #
    """
)
    # write specification on grid
    input_all.write(
    """
# set z-dimension of process grid
procz {}
    """.format('1')
)
    # write input geometry
    input_all.write(
    """
# set mesh file and xlets
mesh {}
inlet -300.0 0.0 0.0 -302.0 0.0 0.0 10.0
outlet 270.0 0.0 0.0 272.0 0.0 0.0 10.0
    """.format("run/plinko_20x.off")
    )
    # write grid spacing
    input_all.write(
        """
# set grid parameters (unit applies to OFF file too!)
gridSpacing {} um
nOverlap 2
supportIBM 4
    """.format(grid)
    )
    # write load balance parameters
    input_all.write(
    """
# set load balance parameters
volumeWeight 0.001
fluidWeight 100.0
wallWeight 5.0
inletWeight 300.0
outletWeight 300.0
    """
    )
    # write regression and debug parameters
    input_all.write(
    """
# # # # # # # regression & debug parameters # # # # # # #

# set optional debugging parameters
verboseTiming 0
printBBoxes 0

# run regression test
regressionTest 0
    """
    )
    # write fluid parameters
    input_all.write(
    """
# # # # # # # # general flow parameters # # # # # # # # #

# set distribution scheme
distScheme AB1k

# set collision kernel
collideKernel basic

# set fluid properties
viscosityKinematic 0.000004
viscosityLBM 0.16666666
densityFluid 1060.0

# # # # # # # # inlet flow parameters # # # # # # # # # #

# set xlet type (must match inletType)
xletType 1

# set inlet type (density vs. velocity vs. volumetric)
inletType velocity
inletVelocity 0.1

# # # # # # # # outlets flow parameters # # # # # # # # #


    """
    )
    # write boundary condition parameters
    input_all.write(
    """
# # # # # # boundary condition parameters # # # # # # # #

# set boundary conditions to BounceBackBCs or RegularizedBCs
boundarycondition BounceBackBCs
    """
    )
    # output parameters
    axes_str = axes_to_str(axes)
    input_all.write(
    """
# # # # # # # # output parameters # # # # # # # # # # # #

# set units for output files
outputUnits real

# set directories, file name, and frequency for LBM output
lbmDataDir run/lbm.iter
lbmDataFile pedata
iprint 10000000000

# set directories, file name, frequency, and coarseness
# for VTU output
lbmVTKDir run/vis_a{size}_s{hard}_{c}.iter
lbmVTKFile dvis
vprint 10000000000
modulusVTU 1

# set directories, file name, frequency, and input file
# for LBM output
sliceDir run/slc_a{size}_s{hard}_{c}.iter
sliceFile slice
sprint 10000000000
slicesDataPath run/plinko_slices

# set shell output for output (0=all, 1=shell, 2=both)
shellOutput 0

# set flag and frequency for time-avg wall shear stress
tawssOutput 0
tawssStepPeriod 1000

# # # # # # # # checkpoint parameters # # # # # # # # # #

# set directory, file name, and frequency for checkpoint
outputDir run
chkptDir check.a{size}_s{hard}_{c}
cprint 10000000000
    """.format(size = axes_str, hard = stiffness, c=coord_str)
    )
    #simulation parameters and cell parameters
    input_all.write(
    """
# # # # # # # # simulation parameters # # # # # # # # # #

# set total number of timesteps
totalsteps {timestep}

# # # # # # # # # # cell parameters # # # # # # # # # #

useIBMCells 1
cellTypes run/celltype_ctc_a{size}_s{hard}.i
cellCoords run/cellcoords_{coo}.i

cellmodel 1
cellRadiusRatio 2.5
ibmPrint 5000
cellWallRepelForce 2.0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    """.format(timestep = 400001, size = axes_str, hard = stiffness, coo=coord_str)
    )
    input_all.close()
    return 0

def help_axes(axes):
    """translate given cell axes into same form as
    celltype file """
    temp = axes * 10 **(-6)
    radius = "{:.8f}".format(temp)
    return radius


def help_Gs(stiffness):
    """translate given stiffness into
    scientific notation that can be put into the
    cell type file"""
    temp = stiffness
    temp *= 10**(-5)
    Gs = "{:.2e}".format(temp)
    return Gs


def input_cell_content(file_name, axes, stiffness):
    """
    this function create celltype_ctc_size_stiffenss.i file
    axes and stiffenss are now the only parameters that can be changed
    """
    input_cell = open("run/" + file_name, "w")
    input_cell.write("name {}\n".format('ctc'))
    input_cell.write("proxyShape ellipsoid\n")
    radius = help_axes(axes)
    input_cell.write("axes {x} {x} {x}\n".format(x = radius))
    input_cell.write("nrefine 3\n")
    Gs = help_Gs(stiffness)
    input_cell.write("shearmod {}".format(Gs))
    input_cell.write("""
skalakmod 100.0
bendingmod 1.0e-18
sponcurv 0.0
elasticconlaw 1
surften 0.0
volpenalty 1.0e-6
shearvisc 0.0
dilationalvisc 0.0
    """)
    input_cell.close()
    return 0


def write_runscript_content(file_name, axes, stiffness, coord_str, input_cell_name):
    runscript = open("{}".format(file_name), "w")
    axes_str = axes_to_str(axes)
    runscript.write(
    """#!/bin/bash
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH -o a{a}_s{s}_{c}.out
#SBATCH -e a{a}_s{s}_{c}.err
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
mpirun -np 128 src/harvey.linux run/{i}
echo "------------------------------------------------------------------------------"
    """.format(a=axes_str, s=stiffness, c=coord_str, i=input_cell_name)
    )
    runscript.close()
    return 0

def write_coord_file(output_file_name, coord):
    coord_file = open("run/{}".format(output_file_name), 'w')
    x = coord[0]
    y = coord[1]
    z = coord[2]
    coord_file.write(
    """ctc {} {} {} 0 0 0
    """.format(x, y, z))
    coord_file.close()
    return 0

def write_file(axes, stiffness, grid_spacing, coord):
    '''
inputs:
coord (list of int): should be in form of [x, y, z]
    '''
    coord_str = coord_to_str([-230, 0, 0])
    file_name = generate_file_name(axes, stiffness, coord_str)
    plinkos = input_all_content(file_name[0], axes, stiffness, grid=grid_spacing, coord_str=coord_str)
    assert plinkos == 0
    cell = input_cell_content(file_name[1], axes, stiffness)
    assert cell == 0
    runscript = write_runscript_content(file_name[2], axes, stiffness, coord_str, input_cell_name=file_name[0])
    assert runscript == 0
    cellcoord = write_coord_file(file_name[3], coord)
    assert cellcoord == 0
    return 0


def main():
    coord = [-230, 0, 0]
    axes = [2.80]
    stiffness = [10]
    grid_spacing = 0.30
    for a in axes:
        a = round(a, 2)
        for b in stiffness:
                write_file(a, b, grid_spacing, coord)
    return 0

if __name__ == "__main__":
    main()
