#!/bin/bash

PROJECT_PATH=/home/marieke/github/TutorialSummerschool

mkdir converted

filenames=$(find $PROJECT_PATH -iname "*.ipynb")
num_files=$(echo "$filenames" | wc -l)
num=0

echo "Converting Jupyter Notebooks..."

for f in $filenames
do
	((num++))
  echo "[$num/$num_files] $f"
	outname=$(echo out$f | tr \/ _).py
	jupyter nbconvert --to python --output=$outname --output-dir=converted $f
done

echo "Extracting requirements..."

pipreqs --debug --savepath=requirements.txt converted

echo "Requirements saved in $(pwd)/requirements.txt"

rm -rf converted/
