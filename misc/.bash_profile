export PERL5LIB=/usr/lib:/usr/X11/lib
#alias exifData_mysql5run='sudo mysql5 --socket=$MYSQL5_SOCKET --user=root --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/import_exifInfoImagePost_Ready.sql' 
#alias pmImport_mysql5run='sudo mysql5 --socket=$MYSQL5_SOCKET --user=root --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/DailyImportTophpMyAdmin_SQL.sql'
#alias postReadyAllImport_mysql5run='sudo mysql5 --socket=$MYSQL5_SOCKET --user=root --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/post_ready_summary.csv_open'
alias run_postReadyAllImport_mysql5='source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/post_ready_summary.csv_open' 
alias run_exifData_mysql5='source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/import_exifInfoImagePost_Ready.sql'
alias run_pmImport_mysql5='source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=root --database=imageMetaData < /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/DailyImportTophpMyAdmin_SQL.sql'
alias apacheAmpps='/Applications/AMPPS/apache/bin/apachectl'
alias sshvbox1='ssh 'jb@192.168.56.101''

#####---->File7 Images Server Vars
export PRODSRV=/mnt/Post_Ready/zProd_Server/imageServer7
export LIBSRV=/mnt/Post_Ready/zProd_Server/imageServer7/lib
export DATASRV=/mnt/Post_Ready/zProd_Server/imageServer7/data
export MAGICK_FOLDER=$PRODSRV/var/magick 
export MAGICK_LOAD=$MAGICK_FOLDER/magick_load
export SCRIPTS=$PRODSRV/scripts
export LIMBO=$PRODSRV/tmp/limbo
export SQLSCRIPTS=$SCRIPTS/sql
export IMGSELECTS=$PRODSRV/images/images_jpg_photoselects
# alias mount_netsrv101=`mount_ftp imagedrop:imagedrop0@netsrv101.l3.bluefly.com $PRODSRV/mnt/netsrv101/`

####---->Image Locations
#export NETSRV101=/mnt/Post_Ready/zProd_Server/imageServer/mnt/netsrv101/images/
export drop_RETOUCHERS=$PRODSRV/tmp/imagedrop/retouchers/
export drop_PHOTOSTUDIO=$PRODSRV/tmp/imagedrop/photostudio/
export archStill=/mnt/Post_Ready/Retouch_Still
export archFashion=/mnt/Post_Ready/Retouch_Fashion
export pushStill=/mnt/Post_Ready/aPhotoPush
export pushFashion=/mnt/Post_Ready/eFashionPush
export tmpPhotoSelects=$PRODSRV/tmp/tmpPhotoSelects
export tmpDeletePhoto=/mnt/Post_Ready/zProd_Server/tmpDeletePhoto


##<--------- ORACLE EnvVars
DYLD_LIBRARY_PATH=/usr/local/oracle/instantclient10_1 
export DYLD_LIBRARY_PATH
TNS_ADMIN=/usr/local/oracle/instantclient10_1
export TNS_ADMIN
ORACLE_HOME=/usr/local/oracle/instantclient10_1/sdk
export ORACLE_HOME
ORACLE_SID=ORCL
export ORACLE_SID
SQLPATH=/usr/local/oracle/instantclient10_1
export SQLPATH
DSSPRDLOGIN='sqlplus -S jbragato/'Blu3f!y'@//192.168.30.66:1531/dssprd1' 
export DSSPRDLOGIN


ZEND_HOME=".:/Applications/AMPPS/www/zend/bin"
ZEND_LIB=".:/Applications/AMPPS/www/zend/library/Zend"
#include_path=".:/Applications/AMPPS/www/zend/library/Zend"



###<----------SQL-PGSQL-ETC.

#export MYSQL5_SOCKET=/Applications/MAMP/tmp/mysql/mysql.sock
export MYSQL_HOME=/usr/local/mysql 
export ODBC_HOME=/Library/ODBC 
export PGSQL_HOME=/Library/PostgreSQL/Versions/9.1.4/bin 
#export PHPRC=/opt/local/etc/php5/php.ini
#export PHPRC=/Applications/AMPPS/php-5.3/etc/php.ini
#export PHPRC=/Applications/AMPPS/php-5.2/etc/php.ini
export MAGICK_CLASS=/Applications/AMPPS/php-5.3/include/php/ext/imagick/imagick_class.c

###<------------ JAVA EnvVars
export JAVA_HOME=/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home 
export JAVA_LIBRARY=/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Libraries
export CLASSPATH=/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes
export PATH="$PATH:$JAVA_HOME/bin:$PERL5LIB:$SQLPATH" 
export JUNIT_HOME=/opt/local/share/java
export ALFRESCOBULKIMPORT 
export CLASSPATH=$CLASSPATH:$JUNIT_HOME/junit.jar 
export ANT_HOME=/opt/local/share/java/apache-ant 
export PATH=${PATH}:${ANT_HOME}/bin 
export JRE_HOME=$JAVA_HOME
export JAVA_JVM_VERSION=1.6
export PATH=${PATH}:${ANT_HOME}/bin
##export CATALINA_HOME=
##export CATALINA_BASE=$CATALINA_HOME/webapps
export EXPATLIBPATH=/opt/local/lib 
export EXPATINCPATH=/opt/local/include

export JETTY_HOME=/opt/local/share/java/jetty-5.1.10
export JETTY_BASE=/opt/local/share/java/jetty-5.1.10/webapps


##<--------Grails & Rails
#export GRAILS_HOME=/Applications/MAMP/grails
#export PATH="$PATH:$GRAILS_HOME/bin"
##[ -r /Applications/MAMP/htdocs/phploader/Grails_bash_completion.txt ] && source /Applications/MAMP/htdocs/phploader/Grails_bash_completion.txt

###<-----My Local Variables
boldText=`tput bold`
normalText=`tput sgr0`
export fileRepo=$PRODSRV/lib/
export TODAY=`date "+%Y-%m-%d"` 
ALFRESCOBULKIMPORT="curl --user 'john_bragato550:sashabea' 'http://192.168.20.242:8080/alfresco/service/bulk/import/filesystem/initiate?sourceDirectory=%2Fmnt%2FPost_Ready%2FzAlfresco_Primary%2Ftmp_Alfresco_Batch_Import_Drop&targetPath=%2FCompany+Home%2FPrimaryImageRepo_1&submit=Initiate+Bulk+Import'"

export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/usr/local/batchRunScripts:$PATH
# MacPorts Installer addition on 2012-06-19_at_12:02:04: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi

export PATH=$PATH:/Applications/Drupal-stack/drush
