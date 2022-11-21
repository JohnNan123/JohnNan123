import array
import gc
import math
import csv
import timeit
import sys
import itertools
import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# readme

# to run:
# python postprocessVtk.py arg1 arg2 arg3 arg4
# where
# arg1 = path to OFF file
# arg2 = path to CSV file from HARVEY
# arg3 = path to vtk file for output
# arg4 = path to 3matic PCA file (optional)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def readOffFile(offFilePath):
	dataCX = offFilePath.readlines()
	# dataCX.pop(1)
	# dataCX.pop(1)
	# dataCX.pop(2)
	meta = dataCX[1].split()
	meta = list(map(int, meta))
	numVtx = meta[0]
	numTri = meta[1]
	vertices = np.zeros((numVtx,3), dtype=np.float64)
	triangles = np.zeros((numTri,3), dtype=np.int)

	for vtxIndex in range(numVtx):
		thisVtx = dataCX[2+vtxIndex].split()
		thisVtx = list(map(float, thisVtx))
		vertices[vtxIndex] = thisVtx

	for triIndex in range(numTri):
		thisTri = dataCX[2+numVtx+triIndex].split()
		thisTri.pop(0)
		thisTri = list(map(int, thisTri))
		triangles[triIndex] = thisTri

	return numVtx, numTri, vertices, triangles

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def readCsvFile(csvFilePath):

	with open(csvFilePath, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		numPts = sum(1 for lines in csvreader)

	pts = np.zeros((numPts,3), dtype=np.float64)
	rho = np.zeros((numPts,1), dtype=np.float64)

	with open(csvFilePath, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		count = 0
		for index, row in enumerate(csvreader):
			row = list(map(float, row))
			pts[index][0] = row[0]
			pts[index][1] = row[1]
			pts[index][2] = row[2]
			rho[index] = row[3]
	return numPts, pts, rho


if __name__ == "__main__":

	startTime = timeit.default_timer()

	# read OFF file
	print("Reading OFF file")
	offFilePath = open(sys.argv[1],"r")
	[numVtx, numTri, vertices, triangles] = readOffFile(offFilePath)
	print("Completed reading OFF file")

	# read CSV file
	print("Reading CSV file")
	csvFilePath = sys.argv[2]
	numPts, pts, rho = readCsvFile(csvFilePath)
	print("Completed reading CSV file")

	fileReadTime = timeit.default_timer()
	print("File read time " + str(fileReadTime - startTime))

	mapVtxData = np.zeros((numVtx,1), dtype=np.int)
	mapVtxData.fill(-1)

	# This is bottleneck for now
	print("Computing nearest neighbor points using KDTree")
	tree = cKDTree(pts)
	for vtxIndex in tqdm(list(range(numVtx))):
		dd, ii = tree.query(vertices[vtxIndex], k=1)
		mapVtxData[vtxIndex] = ii

	mapTime = timeit.default_timer()
	print("Map time " + str(mapTime - fileReadTime))

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	vtkFilePath = sys.argv[3]
	vtkOut = open(vtkFilePath, 'w')

	vtkOut.write("# vtk DataFile Version 2.0 \n")
	vtkOut.write("Test \n")
	vtkOut.write("ASCII \n")
	vtkOut.write("DATASET UNSTRUCTURED_GRID \n")

	vtkOut.write("POINTS " + str(numVtx) + " double \n")
	print("Writing vertices to vtu")
	for vtxIndex in tqdm(list(range(numVtx))):
		vtkOut.write(str(vertices[vtxIndex][0]) + " " + str(vertices[vtxIndex][1]) + " " + str(vertices[vtxIndex][2]) + "\n")

	vtkOut.write("CELLS " + str(numTri) + " " + str(4*numTri) +  "\n")
	print("Writing cells to vtu")
	for triIndex in tqdm(list(range(numTri))):
		vtkOut.write("3 " + str(triangles[triIndex][0]) + " " + str(triangles[triIndex][1]) + " " + str(triangles[triIndex][2]) + "\n")

	vtkOut.write("CELL_TYPES " + str(numTri) +  "\n")
	print("Writing cell types to vtu")
	for triIndex in tqdm(list(range(numTri))):
		vtkOut.write("5\n")

	vtkOut.write("POINT_DATA " + str(numVtx) + "\n")
 
	vtkOut.write("SCALARS ID int \n")
	vtkOut.write("LOOKUP_TABLE default\n")
	print("Writing ffr data to vtu")
	for vtxIndex in tqdm(list(range(numVtx))):
		vtkOut.write(str(0).strip("[]") + "\n")

	vtkOut.write("SCALARS Pressure double \n")
	vtkOut.write("LOOKUP_TABLE default\n")
	print("Writing ffr data to vtu")
	for vtxIndex in tqdm(list(range(numVtx))):
		mapLoc = mapVtxData[vtxIndex]
		myrho = rho[mapLoc]
		vtkOut.write(str(myrho).strip("[]") + "\n")
  
	vtkOut.write("SCALARS WSS double \n")
	vtkOut.write("LOOKUP_TABLE default\n")
	for vtxIndex in range(numVtx):
		mapLoc = mapVtxData[vtxIndex]
		myrho = rho[mapLoc]
		vtkOut.write(str(myrho).strip("[]") + "\n")

	vtkOut.write("VECTORS Velocity double \n")
	for vtxIndex in range(numVtx):
		vtkOut.write(str(0).strip("[]") + " " + str(0).strip("[]") + " " + str(0).strip("[]") + "\n")

	outputTime = timeit.default_timer()
	print("Output time " + str(outputTime - mapTime))

	# finalTime = timeit.default_timer()
	# print("Final time " + str(finalTime - startTime))
