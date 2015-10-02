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


def update_pm_photodate_purepy(colorstyle):
    import requests
    update_url = 'http://dmzimage01.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)
    data= {'sample_image': 'Y', 'photographed_date': 'now'}
    res = requests.put(update_url,data=data)
    return res


if __name__ == '__main__':
    import sys
    r = update_pm_photodate(sys.argv[1])



