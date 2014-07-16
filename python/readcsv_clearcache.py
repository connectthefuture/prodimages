#!/usr/bin/env python
# -*- coding: utf-8 -*-

def formatted_delta_path(flag='csv',textext=None,textpre=None):
    import datetime
    fivedirs = []
    fivecsvs = []
    nowobj = datetime.datetime.now()
    for day in xrange(5):
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


############ Run ###############
def main():
    textpre = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/CSV/'
    textext = '_clearedgecast.csv'
    styles  = []
    delim   = '\n'
    flag    = 'csv'
    
    ## Get Csv files dated today through 5 days ago
    csvfiles = formatted_delta_path(flag=flag,textpre=textpre,textext=textext)
    
    ## Read each csv collecting styles from each row ending with a sorted reversed set of styles to clear
    for f in csvfiles:
        for s in csv_read_file(f,delim):
            styles.append(s)
    styles = reversed([set(sorted(styles[0]))])
    
    ## Finally
    # clear the cache by style list or each style if list too long
    import newAll_Sites_CacheClear
    if len(styles) <= 750:
        newAll_Sites_CacheClear.main(colorstyle_list=styles)
    else:
        for style in styles:
            newAll_Sites_CacheClear.main(colorstyle_list=style)

if __name__ == "__main__":
    main()