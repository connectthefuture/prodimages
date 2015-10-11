#!/usr/bin/env python
# -*- coding: utf-8 -*-

def formatted_delta_path(flag='csv',textext=None,textpre=None,daysrange=1):
    import datetime
    fivedirs = []
    fivecsvs = []
    nowobj = datetime.datetime.now()
    for day in xrange(daysrange):
        delta = datetime.timedelta(weeks=0, days=day, hours=12, minutes=50, seconds=600)
        nowdelta = nowobj - delta
        
        datedir = '{0}{1:%B%d}{2}'.format(textpre, nowdelta, textext)
        datecsv = '{0}{1:%Y-%m-%d}{2}'.format(textpre, nowdelta, textext)
        fivedirs.append(datedir)
        fivecsvs.append(datecsv)
    
    if flag == 'csv':
        return fivecsvs
    else:
        return fivedirs

def csv_read_file(filename, delim):
    import csv
    with open(filename, 'rb') as f:
        # dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, delimiter=delim, dialect='excel')
        rows = []
        for row in reader: 
            rows.append(row)
        return sorted(rows)


def uniq(input_list):
    last = object()
    for item in input_list:
        if item == last:
            continue
        yield item
        last = item

############ Run ###############
def main():
    textpre = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/CSV/'
    textext = '_clearedgecast.csv'
    styles  = []
    delim   = '\n'
    flag    = 'csv'
    daysrange = 3
    ## Get Csv files dated today through 5 days ago
    csvfiles = formatted_delta_path(flag=flag,textpre=textpre,textext=textext,daysrange=daysrange)
    
    ## Read each csv collecting styles from each row ending with a sorted reversed unique list of styles to clear
    for f in csvfiles:
        for s in csv_read_file(f,delim):
            styles.append(s)
    styles = list(uniq(sorted(styles)))
    
    ## Finally
    # clear the cache by style list or each style if list too long
    import newAll_Sites_CacheClear
    #    if len(styles) <= 950:
    #        #styles
    #        newAll_Sites_CacheClear.main(colorstyle_list=styles)
    #    else:
    count = len(styles)
    for style in styles:
        print "{} styles remaining to clear".format(count)
        newAll_Sites_CacheClear.main(colorstyle_list=style)
        count -= 1

if __name__ == "__main__":
    main()