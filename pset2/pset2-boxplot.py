#! /usr/bin/python

# w02-boxplot.py
#   From the supplementary material of Watson et al.
#
#   Generates a boxplot figure showing that mean expression levels
#   of four example sand mouse genes are unchanged in the Coriander
#   mutant, including Coriander itself, which is RNA null.
#
# Usage:
#   python pset2-boxplot.py pset2-data-tidy.tbl pset2-Figure2.png

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

tidyfile     = sys.argv[1]
outfile      = sys.argv[2]

gene_sample  = ['arugula', 'cayenne', 'juniper', 'yam', 'coriander']
data         = pd.read_table(tidyfile, delim_whitespace=True)

# Turns out it's more convenient, for the way we want to use seaborn's
# catplot, to 'melt' the gene name columns into a single column
# that we'll call "gene". Pandas gives us a 'melt' method for this. 
#
data = pd.melt(data, id_vars=['genotype', 'sex'], var_name="gene", value_name="TPM")

# Then we downsample, just the genes in <gene_sample>.
# The Pandas incantation to select rows by a column's value being in a list:
#
data = data.loc[data['gene'].isin(gene_sample)]


# Now we can use Seaborn's catplot conveniently.
#
g = sns.catplot(x="genotype", y="TPM", col="gene", data=data, kind="box", size=4, aspect=0.5, col_wrap=5)
g.set_axis_labels("", "TPM (transcripts per million)")
g.set_titles("{col_name}")
plt.savefig(outfile)