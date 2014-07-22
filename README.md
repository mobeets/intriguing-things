## What this is

Alexis Madrigal's [5 Intriguing Things](https://tinyletter.com/intriguingthings) is a usually-daily newsletter containing links to things. This repo maintains a (good enough) archive of those things, scraped from the emails stored on tinyletter.com.

Currently, the things are stored in data.json. Each day, the script `./scrape_and_push.sh` runs and (if you have the credentials to do so) scrapes the new things, makes a commit, and pushes the updates to this repo. The goal is to eventually have this script run automatically as a heroku worker.
