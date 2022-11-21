#!bin/bash
set -e

echo "Combining slices in: $1"

# remove the old overall.csv if exist or create an enpty one
if test -f "$1/overall.csv"; then
    rm "$1/overall.csv"
fi

# capture all csv files into one array (csv_in_path) in this case
declare -a csv_in_path
csv_in_path=($(ls $1 | grep -e '.csv' | uniq))
echo "csv's in $1: ${csv_in_path[@]}"

# loop though the file
for csv in ${csv_in_path[@]}:
do
# print out the command and file to cat
    echo "cat $1/${csv} >> $1/overall.csv"
    cat $1/${csv} >> $1/overall.csv
done

# sort the overall file based on the id number
sort -n -k0 overall.csv
echo "sort successful"
