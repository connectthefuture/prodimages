#!/usr/bin/env python
# -*- coding: utf-8 -*-

def formatted_delta_path(flag='csv',textext=None):
    import datetime
    
    fivedirs = []
    fivecsvs = []
    nowobj = datetime.datetime.now()
    for day in xrange(5):
        delta = datetime.timedelta(weeks=0, days=day, hours=12, minutes=50, seconds=600)
        nowdelta = nowobj - delta
        
        datedir = '{0:%B%d}{1}'.format(nowdelta, textext)
        datecsv = '{0:%Y-%m-%d}{1}'.format(nowdelta, textext)
        fivedirs.append(datedir)
        fivecsvs.append(datecsv)
    
    if flag == 'csv':
        return fivecsvs
    else:
        return fivedirs


def csv_read_file(filename, delim):
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, delimiter=delim, dialect=dialect)
        rows = []
        for row in reader: 
            rows.append(row)
        return sorted(rows)

############ Run ###############
def main():
    textext = '_clearedgecast.csv'
    print formatted_delta_path(flag='csv',textext=textext)[1]



    ## Finally
    # clear the cache by style
    import newAll_Sites_CacheClear
    newAll_Sites_CacheClear.main(colorstyle_list=styles)

if __name__ == "__main__":
    main()