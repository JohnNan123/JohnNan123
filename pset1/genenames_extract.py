#! /usr/bin/env python3

import re
import sys

# genenames_extract.py
# Get a list of human protein-coding gene names, from a UCSC GTF annotation file.
#
# Usage:
#   ./genenames_extract.py <GTF file>
#
#
# A human genome annotation file, in GTF ("gene transfer format") format, is at:
#    ftp://ftp.ensembl.org/pub/release-85/gtf/homo_sapiens/Homo_sapiens.GRCh38.85.gtf.gz
# To get it:
#    wget ftp://ftp.ensembl.org/pub/release-85/gtf/homo_sapiens/Homo_sapiens.GRCh38.85.gtf.gz
#    gunzip Homo_sapiens.GRCh38.85.gtf.gz
#
# You could get fancier with your Python, with other standard Python modules:
#    gzip   : open a gzip-compressed file directly.
#    urllib : read a file from a URL, without downloading it first
# Using both modules together, I'm pretty sure you could slurp in the UCSC compressed GTF file 
# over the net.

filename = sys.argv[1]

seen = {}                            # seen{'genename'} = True, a dict, keeps track of whether we already have
                                     # this gene name or not. Alas, if we haven't seen it, seen{'nosuchgene'}
                                     # throws an exception, which is not what we want. But the seen.get('nosuchgene)
                                     # method returns None, so it's a better method for testing seen/not seen.

for line in open(filename):
    if line[0] == '#': continue      # Skip comment lines
    line   = line.rstrip('\n')       # Remove the trailing newline
    fields = line.split()            # Split into fields on whitespace
 
    if (fields[2] == 'gene'):        
        # Lines of GTF files have a bunch of optional tags formatted as <key1> "<value1>"; <key2> "<value2>;"
        # Here we use regexp matching to pull out the gene_biotype and gene_name tags, if they're there.
        m1 = re.search(r'gene_biotype\s*"([^"]+)";', line)    # r'...' is a raw string: 
        m2 = re.search(r'gene_name\s*"([^"]+)";',    line)    #  you can use regexp metachars w/o escaping them.
        if m1 and m2:
            biotype  = m1.group(1)  # biotypes include "protein_coding"
            genename = m2.group(1)  
            if biotype == 'protein_coding':
                if not seen.get(genename):     
                    print(genename)
                    seen[genename] = True


