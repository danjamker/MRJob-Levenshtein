#!/usr/bin/env bash
python MRLevenshtein.py  -r hadoop -v hdfs://user/kershad1/reddit-innovations -o ./output/1 --wordlist ./Data/words --no-output --conf-path .mrjob.conf