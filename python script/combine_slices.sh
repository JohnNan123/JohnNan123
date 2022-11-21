#!/bin/bash
# fail script on first error
set -e

echo "Combining slices in: $1"

declare -a unqiue_lbms
unqiue_lmbs=($(ls $1 | grep -E 'lbm*\.csv' | cut -d. -f1 | uniq))

echo "Unique lbms: ${unqiue_lbms[@]}"

# now loop through the unqiue slices
for slc in "${unqiue_lbms[@]}"
do
    # print out command before doing it
    echo "cat $1/${slc}.slice.*.csv > $1/${slc}.slice.csv"
    cat $1/${slc}.slice.*.csv > $1/${slc}.slice.csv
done
