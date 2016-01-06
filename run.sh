#!/usr/bin/env bash
python MRLevenshtein.py  -r hadoop -v ./Data/words -o ./output/1 --wordlist ./Data/words --no-output --conf-path .mrjob.conf