#!/usr/bin/env python

import csv
import sys
import os

searchdir = sys.argv[0]

readcsvf = sys.argv[1]

with open(readcsvf) as f:
        reader = csv.DictReader(f)
        for line in reader:
                source = line[0]
                dest   = line[1]
                os.rename(source, dest)