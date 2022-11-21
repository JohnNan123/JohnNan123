# make-fig-grid.py
#
# Make the figure showing Student's grid, w/ a dart in it.  Also
# serves as a starting example of plotting a heat map in Seaborn.
#
# Usage:
#    python make-fig-grid.py <outfile.png>
#
# Example:
#    python make-fig-grid.py fig-grid.png
#

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

outpng = sys.argv[1]    # get output filename from command line

# Set up the x and y coords
gridrows = np.linspace( 100.0,   5.0, 20)   # rows of the board: std. dev., sigma
gridcols = np.linspace(-100.,  100.0, 21)   # cols of the board: mean (location), mu
nrows    = len(gridrows)
ncols    = len(gridcols)

# "Data" are all zeros, with one 1.0 at (5,15)
data = np.zeros((nrows, ncols))             # Initializes a numpy "n-D array" (ndarray)
data[5, 15] = 1.0
        
# Format axis labels as strings, with values as "10" not "10.0" for clarity, space
xlabels = [ "{0:.0f}".format(val) for val in gridcols ]
ylabels = [ "{0:.0f}".format(val) for val in gridrows ]

# the Seaborn "heatmap" plot
# with some examples of how it can be customized.
#
ax = sns.heatmap(data,                 # takes a 2D array of data
                 xticklabels=xlabels,  #   ... set custom x axis labels
                 yticklabels=ylabels,  #   ... set custom y axis labels
                 cbar=False,           #   ... turn off the default color scale bar
                 square=True,          #   ... force the plot to be square
                 linecolor='grey',     #   ... set grid line color
                 linewidth=0.5)        #   ... set grid line width

# now we have an Axes object that Seaborn returned to us,
# and we can do additional customization, like...

ax.set(xlabel='$\mu$',                 # ...set X axis label, using LaTeX formatting
       ylabel='$\sigma$')              # ...and Y axis label
for label in ax.get_yticklabels():    
    label.set_size(10)                 # ... and font size on y-axis tick labels
for label in ax.get_xticklabels():    
    label.set_size(10)                 # ... and on x-axis tick labels

# Finally, we save the whole Figure to a file.
plt.savefig(outpng)


