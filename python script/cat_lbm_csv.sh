#!/bin/bash
set -e
echo "Combining slices in: $1"

declare -a unique_lbms
unique_lbms=($(ls $1))

echo "Unique lbms: ${unique_lbms[@]}"

# now loop through the unqiue slices
for slc in "${unique_lbms[@]}"
do
    # print out command before doing it
    echo "cat $1/${slc}/*.csv > $1/${slc}.csv"
    cat $1/${slc}/*.csv > $1/${slc}.csv
done
