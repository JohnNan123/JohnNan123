#! /usr/bin/python

# Supplementary script
# From Holmes et al., "The adventure of the missing phenotype", Sand Mouse Journal 1:2 (2022)
#
# Usage: 
#   python pset2-validate.py pset2-data.tbl
#

import sys

datafile    = sys.argv[1]
n           = 0

for line in open(datafile):          # For each line in the input file...
    n += 1                           # Track line number
    line   = line.rstrip('\n')       # Remove the trailing newline
    if line[0] == '#': continue      # Skip comment lines
    fields = line.split()            # Split into fields on whitespace

    if fields.count('BAD_DATA') > 0: # Look for bad data
        sys.exit('bad data detected at line {}:\n   {}'.format(n, line))

print('No errors detected in file.')
