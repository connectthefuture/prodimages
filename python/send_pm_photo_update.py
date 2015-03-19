#!/usr/bin/env python
import os, sys, re, csv

def update_pm_photodate(colorstyle):
    import subprocess
    update_url = 'http://dmzimage01.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)

    subprocess.call([
    "curl",
    '-d',
    "sample_image=Y",
    '-d',
    "photographed_date=now",
    "-X",
    "PUT",
    "-format",
    update_url,
    ])

if __name__ == '__main__':
    import sys
    r = update_pm_photodate(sys.argv[1])



