#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Merges
def sqlQueryMergedStyles():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    q = '''
        SELECT POMGR_SNP.ADT_COLORSTYLE_MERGE.TRG_PRODUCTCOLOR_ID AS "current_style",
        POMGR_SNP.ADT_COLORSTYLE_MERGE.SRC_PRODUCTCOLOR_ID AS "voided_style",
        POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE AS "merge_date", POMGR_SNP.USERS.USERNAME AS "username"
        FROM POMGR_SNP.ADT_COLORSTYLE_MERGE INNER JOIN POMGR_SNP.USERS ON POMGR_SNP.ADT_COLORSTYLE_MERGE.USER_ID = POMGR_SNP.USERS.ID
        ORDER BY POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE DESC
        '''
    result = connection.execute(q)
    merged_styles = {}
    voided_styles = []
    for row in result:
        merged_style = {}
        merged_style['current_style'] = str(row['current_style'])
        merged_style['voided_style']  = str(row['voided_style'])
        voided_styles.append(row['voided_style'])
        merged_style['username'] = row['username']
        merged_style['merge_dt'] = row['merge_date']
        merged_styles[str(row['current_style'])] = merged_style
    connection.close()
    return merged_styles, list(sorted(voided_styles))


def get_using_python(destdir,sqlcolorstyles):
    import os,shutil,datetime,re
    regex_pending = re.compile(r'^.+?/PENDING/.+?\.jpg')

    merged_styles=sqlQueryMergedStyles()[1]
    ncount = 0
    mcount = 0

    for row in sqlcolorstyles:
        if row:
            try:
                file_path = row[0]
                file_name = file_path.split('/')[-1]
                colorstyle = file_name[:9]
                ## Destination File name if not in a PENDING dir
                dest_file = os.path.join(destdir,file_name)

                ### Separate anything the a is Pending a second shot from Still Life
                ##  also remove any merges
                try:
                    if merged_styles.index(int(colorstyle)):
                        mcount += 1
                        print mcount, ' MCOUNT ', file_path
                    elif re.findall(regex_pending, file_path):
                        pending_folder = os.path.join(destdir,'PENDING')
                        ## Make the pending dir in today
                        if not os.path.isdir(pending_folder):
                            os.mkdir(pending_folder, 16877)
                        dest_file = os.path.join(pending_folder, file_name)
                except ValueError:
                    shutil.copy2(file_path, dest_file)
                    # os.chmod(dest_file,00755)
                    # rowlist.append(cmdargs)
                    ncount += 1
                    print "Files Found: {0},\t File Name: {1}".format(ncount,file_name)
            except:
                print "Failed {0}".format(row)

    print 'Final ', ncount, ' Mcount ', mcount
    return ncount,mcount


############ RUN ########################
def main():
    import os,sqlalchemy,shutil,datetime,re,glob
    import mtags_reshoots
    mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@localhost:3301/data_imagepaths')
    connection = mysql_engine.connect()
    ###

    #daily_incomplete_query = '''SELECT t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt` FROM `data_imagepaths`.`push_photoselects` t1 join `www_django`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle` having (t2.`image_ready_dt` = '0000-00-00' or t2.`image_ready_dt` is null) ORDER BY t1.`file_path` ASC'''
    daily_incomplete_query="""
        SELECT t1.`file_path`,
        t1.`colorstyle`, t2.`image_ready_dt` FROM `www_django`.`push_photoselects` t1
        join `www_django`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle`
        where
            (t1.photo_date BETWEEN SYSDATE( ) - INTERVAL 15 DAY AND SYSDATE( ) + INTERVAL 2 DAY
            OR t1.`photo_date` = '0000-00-00')
            AND t2.`image_ready_dt` is null
        ORDER BY t1.`file_path` ASC;
        """

    daily_reshoot_query = """
        select distinct data.`file_path`, data.`photo_date`, data.`colorstyle`, CONCAT('/mnt/Post_Ready', t3.`file_path`),t3.`photo_date`
        FROM
            (SELECT t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt` , t1.`photo_date`,t1.alt
            FROM `www_django`.`push_photoselects` t1
            join `www_django`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle`
            where t1.photo_date BETWEEN SYSDATE( ) - INTERVAL 15 DAY AND SYSDATE( ) + INTERVAL 2 DAY
            having (t2.`image_ready_dt` != '0000-00-00' or t2.`image_ready_dt` is not null))
        AS data
        join `data_imagepaths`.`post_ready_original` t3 on data.`colorstyle` = t3.`colorstyle`
        where data.`image_ready_dt` < t3.`photo_date` and data.`alt` = t3.`alt`;
        """
    ###

    result = connection.execute(daily_incomplete_query)
    result_reshoot = connection.execute(daily_reshoot_query)

    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    today_folder = os.path.join('/mnt/Post_Ready/Daily', today)
    today_folder_reshoot = os.path.join(today_folder, 'reshoot')

    try:
        os.makedirs(today_folder, 16877)
        os.makedirs(today_folder_reshoot, 16877)
    except:
        pass
    try:
        os.makedirs(today_folder_reshoot, 16877)
    except:
        pass

    destdir = today_folder
    destdir_reshoot = today_folder_reshoot

    # Get Incomplete
    get_using_python(destdir,result)
    # Get Reshoots
    get_using_python(destdir_reshoot,result_reshoot)

    reshoots = glob.glob(os.path.join(destdir_reshoot,'*.jpg'))
    if reshoots:
        print reshoots
        for f in reshoots:
            try:
                mtags_reshoots.main(filename=f)
            except AttributeError:
                pass
    else:
        os.rmdir(destdir_reshoot)


if __name__ == '__main__':
    main()
