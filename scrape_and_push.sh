#!/bin/bash

now=$(date +"%Y/%m/%d")
git clone https://github.com/mobeets/intriguing-things.git
# git clone ssh://git@github.com/mobeets/intriguing-things.git
cd intriguing-things
python model.py --infile data.json --outfile data.json
git add .
git commit -m "data update ($now)"
git remote set-url origin https://$GITHUB_USERNAME:$GITHUB_PASSWORD@github.org/mobeets/intriguing-things.git
git push origin gh-pages
cd ..
rm -rf intriguing-things
