#! /usr/bin/python

# Usage:
#   pset3-visualize.py <infile> <fig.png>
#
# Example:
#   pset3-visualize.py pset3-data.tbl foo.png
#
# Reads pset3-data.tbl; produces a figure in <fig.png> that visualizes the
# five true clusters.

import matplotlib.pyplot as plt
import numpy             as np
import sys
import scipy.stats as stats
import scipy.misc as misc

# Grab necessary file names from the call to python
infile = sys.argv[1]
outfile = sys.argv[2]

def read_data(infile):
    '''
    read_data(infile)
    Read Lestrade's input file, pset3-data.tbl, or a file in that format.
    Return:
       ctype[0..N-1] : cell types 0..Q-1 for each cell i
       data[i,g]     : array of count data; rows = cells i; cols = genes g
       N             : number of cells (rows of the data file)
       G             : number of genes (cols of the data file, after the first)
       Q             : number of cell types
    '''
    ctype = []
    data  = []
    with open(infile) as f:
        for line in f:
            if line[0] == '#': continue   # skip comment lines
            fields = line.split()
            ctype.append(int(fields[1]))
            data.append( [int(fields[2]), int(fields[3])])  # Note: assumes exactly 2 genes
    ctype = np.array(ctype)
    data  = np.array(data)
    N, G  = np.shape(data)
    Q     = np.max(ctype) + 1
    return ctype, data, N, G, Q


def initialize_at_true():
    '''
    initialize_at_true():
    Returns the true mu centroids, and the true proportions;
       mu[q,g]  : array of means for mixture q, gene g
       qp[q]    : mixture coefficient for mixture q
    '''
    qp = np.array([ 0.1, 0.2, 0.4, 0.2, 0.1 ])
    mu = np.array([[   30., 2000. ],
                   [ 2000., 2000. ],
                   [  300.,  300. ],
                   [   30.,   30. ],
                   [ 2000,    30. ]])
    return mu, qp


def visualize_data(data, mu, C):
    '''
    visualize_data():

    This might give you a starting point that saves some matplotlib
    boiler plate

    Input:
       data[i,g] : count data for each cell i, for each gene g
       mu[q,g]   : array of mean counts for mixture q, gene g
       C[i]      : assignment of cell i to a cluster 0..Q-1
       outpng    : save figure to PNG file (must end in .png; example 'foo.png')

    '''
    N, G  = np.shape(data)
    Q, G2 = np.shape(mu)
    assert G == G2
    assert len(C) == N

    # The Tableau20 color palette, prettier than matplotlib defaults.
    TableauColor = { 
        'red':           (0.839, 0.153, 0.157),
        'blue':          (0.122, 0.467, 0.706),
        'green':         (0.173, 0.627, 0.173),
        'orange':        (1.000, 0.498, 0.055),
        'peach':         (1.000, 0.733, 0.471),
        'purple':        (0.580, 0.404, 0.741),
        'lightpurple':   (0.773, 0.690, 0.835),
        'violet':        (0.890, 0.467, 0.761),
        'peagreen':      (0.737, 0.741, 0.133),
        'lightpeagreen': (0.859, 0.859, 0.553),
        'aqua':          (0.090, 0.745, 0.812),
        'pink':          (0.969, 0.714, 0.824),
        'salmon':        (1.000, 0.596, 0.588),
        'lightaqua':     (0.620, 0.855, 0.898),
        'lightbrown':    (0.769, 0.612, 0.580),
        'grey50':        (0.498, 0.498, 0.498),
        'grey20':        (0.780, 0.780, 0.780),
        'lightgreen':    (0.596, 0.875, 0.541),
        'brown':         (0.549, 0.337, 0.294),
        'lightblue':     (0.682, 0.780, 0.910),
    }
    
    # We can assign colors to up to Q=10 components with this colormap. if you want more, add more.
    colormap = ['orange', 'lightgreen', 'red', 'aqua', 'brown', 'peach', 'blue', 'lightpurple', 'peagreen', 'salmon']

    fig, ax = plt.subplots()
    for i in range(N):
        edgecolor = TableauColor[ colormap[ C[i]]]
        fillcolor = 'w'
        shape     = 'o'
        ax.loglog( data[i,0], data[i,1], marker=shape, mec=edgecolor, mfc=fillcolor, mew=1.5)

    for q in range(Q):
        ax.loglog(mu[q,0], mu[q,1], '*k', ms=10)

    ax.set_xlabel('caraway (counts)')
    ax.set_ylabel('kiwi (counts)')

    return fig

# Run it
ctype, data, N, G, Q = read_data(infile)
centroids, qp = initialize_at_true()
f = visualize_data(data, centroids, ctype)

f.savefig(outfile, dpi=200, transparent=False)


