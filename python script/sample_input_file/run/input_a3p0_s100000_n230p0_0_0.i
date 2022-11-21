
# # # # # # # # input file for new HARVEY # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Version: September 2017  # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # grid setup parameters # # # # # # # # #
    
# set z-dimension of process grid
procz 1
    
# set mesh file and xlets
mesh run/plinko_20x.off
inlet -300.0 0.0 0.0 -302.0 0.0 0.0 10.0
outlet 270.0 0.0 0.0 272.0 0.0 0.0 10.0
    
# set grid parameters (unit applies to OFF file too!)
gridSpacing 0.3 um
nOverlap 2
supportIBM 4
    
# set load balance parameters
volumeWeight 0.001
fluidWeight 100.0
wallWeight 5.0
inletWeight 300.0
outletWeight 300.0
    
# # # # # # # regression & debug parameters # # # # # # #

# set optional debugging parameters
verboseTiming 0
printBBoxes 0

# run regression test
regressionTest 0
    
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


    
# # # # # # boundary condition parameters # # # # # # # #

# set boundary conditions to BounceBackBCs or RegularizedBCs
boundarycondition BounceBackBCs
    
# # # # # # # # output parameters # # # # # # # # # # # #

# set units for output files
outputUnits real

# set directories, file name, and frequency for LBM output
lbmDataDir run/lbm.iter
lbmDataFile pedata
iprint 10000000000

# set directories, file name, frequency, and coarseness
# for VTU output
lbmVTKDir run/vis_a3p0_s100000_n230p0_0_0.iter
lbmVTKFile dvis
vprint 5000
modulusVTU 1

# set directories, file name, frequency, and input file
# for LBM output
sliceDir run/slc_a3p0_s100000_n230p0_0_0.iter
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
chkptDir check.a3p0_s100000_n230p0_0_0
cprint 10000000000
    
# # # # # # # # simulation parameters # # # # # # # # # #

# set total number of timesteps
totalsteps 5000001

# # # # # # # # # # cell parameters # # # # # # # # # #

useIBMCells 1
cellTypes run/celltype_ctc_a3p0_s100000.i
cellCoords run/cellcoords_n230p0_0_0.i

cellmodel 1
cellRadiusRatio 2.5
ibmPrint 1000
cellWallRepelForce 2.0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    