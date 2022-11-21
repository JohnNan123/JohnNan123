#! /usr/bin/env python3

# figure1.py 
# Supplementary methods from 'The case of the dead sandmouse', Moriarty
# et al., Cool 1:1 (2020).
#
# Usage:
#   ./figure1.py Moriarty_SuppTable1 <output.png>


import matplotlib.pyplot as plt
import numpy as np
import sys

tpmfile = sys.argv[1]
outfile = sys.argv[2]

timepoints = [0, 12, 24, 48, 96]
tpmdata    = {}                        # We'll build a dict of lists, tpmdata['genename'][j]
                                       #  for 5 time points j=0..4
for line in open(tpmfile):
    if line[0] == '#': continue     
    line   = line.rstrip('\n')      
    fields = line.split()           

    tpmdata[fields[0]] = [float(s) for s in fields[1:6]]


# I looked at Moriarty_SuppTable1 to choose four genes, such that
# gene 0 goes down, gene 1 peaks @ 24h,  2 peaks @48h, 3 rises.
#
#  awk '$2 > $3 && $3 > $4' Moriarty_SuppTable1
#  awk '$2 < $3 && $3 < $4 && $4 > $5 && $4/$3 > 1.3' Moriarty_SuppTable1
#  awk '$2 < $3 && $3 < $4 && $4 < $5 && $5 > $6 && $5/$6 > 1.4 && $5/$4 > 1.3' Moriarty_SuppTable1
#  awk '$2 < $3 && $3 < $4 && $4 < $5 && $5 < $6' Moriarty_SuppTable1 
#
genes  = ['tomato', 'MLX', 'ANAPC15', 'chestnut']
for i,g in enumerate(genes):
    plt.subplot(2, 2, i+1)
    plt.plot(timepoints, tpmdata[g], 
             marker='o',
             markerfacecolor='w', 
             markeredgecolor=('xkcd:orange'),
             markeredgewidth=2,
             color=('xkcd:orange'), 
             linewidth=2)
    plt.title('({})'.format('ABCD'[i]), loc='left')
    plt.title('{}'.format(g), loc='right')
    plt.xticks(timepoints)

    # Here I'm manually setting the y axis tick labels, having looked at their range.
    # Deliberately setting all different, to set a bad example.
    if i == 0:                          
        plt.yticks(np.arange(0, 155, 25))       # fig, 0.1-100    (remember, arange() is [), half-open)
    elif i == 1:
        plt.yticks(np.arange(100, 255, 25))       # MLX, 116-180. Deliberately not using 0 baseline, to make a point
    elif i == 2:
        plt.yticks(np.arange(0, 55, 10))        # ANAPC15, 14-32
    elif i == 3:
        plt.yticks(np.arange(0, 805, 100))     # chestnut, 100-600

    if i >= 2:      plt.xlabel('time (hr)')
    if i % 2 == 0 : plt.ylabel('expression (tpm)')

plt.tight_layout()
plt.savefig(outfile)

    
    
    
  
