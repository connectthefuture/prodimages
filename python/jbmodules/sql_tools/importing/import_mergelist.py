#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on sun March 18 14:48:56 2014

@author: jbragato
"""
#orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')

def sqlQueryMergedStyles():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    q = '''SELECT POMGR_SNP.ADT_COLORSTYLE_MERGE.TRG_PRODUCTCOLOR_ID AS "current_style", POMGR_SNP.ADT_COLORSTYLE_MERGE.SRC_PRODUCTCOLOR_ID AS "voided_style", POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE AS "merge_date", POMGR_SNP.USERS.USERNAME AS "username" FROM POMGR_SNP.ADT_COLORSTYLE_MERGE INNER JOIN POMGR_SNP.USERS ON POMGR_SNP.ADT_COLORSTYLE_MERGE.USER_ID = POMGR_SNP.USERS.ID ORDER BY POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE DESC'''
    result = connection.execute(q)
    merged_styles = {}
    for row in result:
        merged_style = {}
        merged_style['current_style'] = row['current_style']
        merged_style['voided_style']  = row['voided_style']
        merged_style['username'] = row['username']
        merged_style['merge_dt'] = row['merge_date']
        merged_styles[str(row['current_style'])] = merged_style
    connection.close()
    return merged_styles


def main():
    #### Run Import To Mysql
    import sys
    import os
    import sqlalchemy


    merged_styles = sqlQueryMergedStyles()
    print "Merge Gotten"

    ## Truncate Prior to Inserting new data
    #mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
    #connection1 = mysql_engine.connect()
    #trunc_table = """TRUNCATE TABLE asset_status"""
    #connection1.close()

    ## Trunc www_django vers wont TRUNC du to Foreign Keys
    #mysql_engine_dj  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    #connectiondj = mysql_engine_dj.connect()
    #trunc_table = """TRUNCATE TABLE asset_status"""
    #connectiondj.close()


    for k,v in merged_styles.iteritems():
        import datetime
        print "Off"
        try:
            mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imports')
            mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection_data = mysql_engine_data.connect()
            #connection_www = mysql_engine_www.connect()
            print "Connext"
            try:
                print "Begin Execute"
                connection_data.execute("""INSERT INTO merged_styles (current_style, voided_style, username, merge_dt) VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                            current_style       = VALUES(current_style),
                            username           = VALUES(username),
                            merge_dt           = VALUES(merge_dt);
                            """, str(k), v['voided_style'], v['username'], v['merge_dt'])
                print "Successful Insert asset_status --> {0}".format(k)
            except sqlalchemy.exc.IntegrityError:
                print "Duplicate Entry {0}".format(k)
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        except sqlalchemy.exc.DatabaseError:
            print "DBERR \t" + k
            pass


if __name__ == '__main__':
    main()

