#!/usr/bin/env python
# -*- coding: utf-8 -*-
    
def get_using_python(destdir,sqlcolorstyles):
    import os,shutil,datetime,re
    regex_pending = re.compile(r'^.+?/PENDING/.+?\.jpg')


    ncount = 0
    for row in sqlcolorstyles:
        if row:
            try:
            
                file_path = row[0]
                file_name = file_path.split('/')[-1]
     
                ## Destination File name if not in a PENDING dir
                dest_file = os.path.join(destdir,file_name)
                
                ### Separate anything the is Pending a second shot from Still Life
                if re.findall(regex_pending, file_path):
                    pending_folder = os.path.join(destdir,'PENDING')
                    ## Make the pending dir in today
                    if not os.path.isdir(pending_folder):
                        os.mkdir(pending_folder, 16877)
                    dest_file = os.path.join(pending_folder, file_name)
                    
                shutil.copy2(file_path, dest_file)
                #os.chmod(dest_file,00755)
                #rowlist.append(cmdargs)
                ncount += 1
                print "Files Found: {0},\t File Name: {1}".format(ncount,file_name)
                
            except:
                print "Failed {0}".format(file_path)
 

############ RUN ########################
def main():
    import os,sqlalchemy,shutil,datetime,re,glob
    mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@localhost:3301/data_imagepaths')
    connection = mysql_engine.connect()   
    daily_incomplete_query = '''SELECT t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt` FROM `data_imagepaths`.`push_photoselects` t1 join `data_imagepaths`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle` having (t2.`image_ready_dt` = '0000-00-00') ORDER BY t1.`file_path`  ASC '''


    #daily_incomplete_query = '''SELECT t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt` FROM `data_imagepaths`.`push_photoselects` t1 join `data_imagepaths`.`product_snapshot` t2 on t1.`colorstyle` = t2.`colorstyle` having (t2.`image_ready_dt` = '0000-00-00') ORDER BY t1.`file_path`  ASC '''

    result = connection.execute(daily_incomplete_query)


    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    today_folder = os.path.join('/mnt/Post_Ready/Daily', today)
    today_folder_reshoot = os.path.join('/mnt/Post_Ready/Daily', today, 'reshoot')

    try:
        os.mkdir(today_folder, 16877)
        os.mkdir(today_folder_reshoot, 16877)
    except:
        pass

    destdir = today_folder
    destdir_reshoot = today_folder_reshoot
    
    # Get Incomplete
    get_using_python(destdir,sqlcolorstyles)
    # Get Reshoots
    get_using_python(destdir_reshoot,sqlcolorstyles)
    if glob.glob(os.path.join(destdir_reshoot,'*.jpg')):
        pass
    else:
        os.rmdir(destdir_reshoot)

if __name__ == '__main__':
    main()
