#!/bin/bash
now=$(date +"%Y/%m/%d")
git clone https://github.com/$GITHUB_USERNAME/intriguing-things.git
cd intriguing-things
python model.py --infile data.json --outfile data.json
git add .
git commit -m "data update ($now)"
git remote set-url origin https://$GITHUB_USERNAME@github.com/$GITHUB_USERNAME/intriguing-things.git
# expect "assword:"
# send '$GITHUB_PASSWORD\n';
# interact
git push origin gh-pages
cd ..
rm -rf intriguing-things
