#!/usr/bin/env python
import os, sys, re, csv

def update_pm_photodate_purepy(colorstyle):
    import requests
    update_url = 'http://dmzimage01.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)
    data= {'sample_image': 'Y', 'photographed_date': 'now'}
    res = requests.put(update_url,data=data)
    return res


if __name__ == '__main__':
    import sys, re
    try:
        valid_colorstyle = sys.argv[1]
        if len(valid_colorstyle) == 9 and valid_colorstyle.isdigit():
            r = update_pm_photodate_purepy(valid_colorstyle)
            if r.status_code == 200:
                print 'Successfully Sent... ', valid_colorstyle
            else:
                print 'Backend Issue Prevented Sending Data... ', r
        else:
            raise IndexError()
    except IndexError:
        print('You need to provide a valid 9-digit Colorstyle,\vbut you didnt.')

