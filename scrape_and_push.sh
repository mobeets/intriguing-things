#!/bin/bash

now=$(date +"%Y/%m/%d")
git clone https://github.com/mobeets/intriguing-things.git
cd intriguing-things
python model.py --infile data.json --outfile data.json
git add .
git commit -m "data update ($now)"
git push origin gh-pages
cd ..
rm -rf intriguing-things
