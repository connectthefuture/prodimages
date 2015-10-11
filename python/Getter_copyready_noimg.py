#!/usr/bin/env python

import os,sqlalchemy,shutil,datetime
mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@localhost:3301/data_imagepaths')
connection = mysql_engine.connect()   
daily_incomplete_query = '''SELECT t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt`, t2.`copy_ready_dt` FROM `www_django`.`push_photoselects` t1 join `www_django`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle` where (t2.`image_ready_dt` is null and t2.`copy_ready_dt` is not null) ORDER BY t1.`file_path` ASC'''

result = connection.execute(daily_incomplete_query)


dt = str(datetime.datetime.now())
today = dt.split(' ')[0]
today_folder = os.path.join('/mnt/Post_Ready/Daily', today + '_copy')
try:
    os.mkdir(today_folder, 16877)
    #os.chmod(today_folder,00755)
except:
    pass
        


ncount = 0
for row in result:
    if row:
        try:
        
            import os,sqlalchemy,shutil,datetime
            #dt = str(datetime.datetime.now())
            #today = dt.split(' ')[0]
            #today_folder = os.path.join('/mnt/Post_Ready/Daily', today)
            file_path = row[0]
            file_name = file_path.split('/')[-1]
            #cmdargs = file_path, os.path.join(today_folder, file_name)
            dest_file = os.path.join(today_folder, file_name)
            shutil.copy2(file_path, dest_file)
            #os.chmod(dest_file,00755)
            #rowlist.append(cmdargs)
            ncount += 1
            print "Files Found: {0},\t File Name: {1}".format(ncount,file_name)
            
        except:
            print "Failed {0}".format(file_path)
            


#def ntuples(lst, n):
#    return zip(*[lst[i:]+lst[:i] for i in range(n)])
        
#newtuplist = ntuples(rowlist,n)
#print len(newtuplist)
        
