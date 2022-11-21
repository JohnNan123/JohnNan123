import matplotlib.pyplot as plt
import os
import math
import numpy as np

class vtk_tag():
    def __init__(self, name, time, path, points=None, velocity=None, force=None):
        self.name = name
        self.time = time
        self.path = path
        self.points = dict() if points is None else points
        self.velocity = dict() if velocity is None else velocity
        self.force = dict() if force is None else force

    def analysis(self):
        num_points = self.points['total_points']
        # calculate net force
        netx_f = sum(self.force['x']) / num_points
        nety_f = sum(self.force['y']) / num_points
        netz_f = sum(self.force['z']) / num_points
        self.net_force = (netx_f, nety_f, netz_f)

        # calculate net velocity
        netx_v = sum(self.velocity['x']) / num_points
        nety_v = sum(self.velocity['y']) / num_points
        netz_v = sum(self.velocity['z']) / num_points
        self.net_velocity = (netx_v, nety_v, netz_v)

        # calculate cell center
        netx = sum(self.points['x']) / num_points
        nety = sum(self.points['y']) / num_points
        netz = sum(self.points['z']) / num_points
        self.center = (netx, nety, netz)

        # calculate mass_distribution
        count = 0
        for points in self.points['y']:
            if points >= self.center[1]:
                count += 1
            else:
                continue
        upper_present = count / num_points
        lower_present = 1 - upper_present
        self.mass_distribution = (upper_present, lower_present)


def gene_vtk (path, name, cell_id, timestep):
    name = name
    path = path + "/vis_cell_" + name + ".iter/"
    filename = path + str(cell_id) + "." + str(timestep * 5000) + ".vtk"
    time = timestep
    vtk = vtk_tag(name=name, time= time, path= filename)
    return vtk


def read_vtk (path, name, cell_id, timestep):
    vtk = gene_vtk(path, name, cell_id, timestep)
    vtk_file = open(vtk.path, 'r')
    count = 0 # gives the number of line reading

    # initialize the range to read to be a big number
    # the number will be changed if the line has been read
    start_v = 1000000
    end_v = 1000000
    start_f = 1000000
    end_f = 1000000

    # initialize vtk.points class
    vtk.points['x'] = []
    vtk.points['y'] = []
    vtk.points['z'] = []

    #initializ vtk.velocity class
    vtk.velocity['x'] = []
    vtk.velocity['y'] = []
    vtk.velocity['z'] = []

    #initializ vtk.force class
    vtk.force['x'] = []
    vtk.force['y'] = []
    vtk.force['z'] = []

    while True:
        count += 1
        # Get next line from file
        line = vtk_file.readline()

        # find the line of position:
        if count == 5:
            line_split = line.split(' ')
            total_points = int(line_split[1])
            vtk.points['total_points'] = total_points

        # store position information into vtk.point
        if count > 5 and count <= 5 + total_points:
            line_split = line.split(' ')
            position_x = float(line_split[0])
            position_y = float(line_split[1])
            position_z = float(line_split[2])
            vtk.points['x'].append(position_x)
            vtk.points['y'].append(position_y)
            vtk.points['z'].append(position_z)

        # store the velocity information:
        if line == 'VECTORS Velocity double\n':
            start_v = count
            end_v = count + total_points

        if count > start_v and count <= end_v:
            line_split = line.split(' ')
            velocity_x = float(line_split[0])
            velocity_y = float(line_split[1])
            velocity_z = float(line_split[2])
            vtk.velocity['x'].append(velocity_x)
            vtk.velocity['y'].append(velocity_y)
            vtk.velocity['z'].append(velocity_z)

        # store the force information:
        if line == 'VECTORS Force double\n':
            start_f = count
            end_f = count + total_points

        if count > start_f and count <= end_f:
            line_split = line.split(' ')
            force_x = float(line_split[0])
            force_y = float(line_split[1])
            force_z = float(line_split[2])
            vtk.force['x'].append(force_x)
            vtk.force['y'].append(force_y)
            vtk.force['z'].append(force_z)


        # if line is empty, end of file is reached
        if not line:
            break

    vtk_file.close()
    return vtk
