<?php
//$db_local_hostname = "192.168.2.110:3306";
//$db_local_hostname = "127.0.0.1:3301";
//$db_local_hostname = "192.168.2.111:3306";
$db_local_hostname = "127.0.0.1:3301";
    

//$db_local_hostname = ":/var/run/mysqld/mysqld.sock";
$db_local_username = 'root';
$db_local_password = 'root';
////---Available tables and databases--attach to master table/database variable--///

//$db_local_dbDataImagePaths = 'data_imagepaths';
//$db_local_dbDataImports = 'data_imports';
//$db_local_dbDataMetadata = 'data_metadata';
//$db_local_dbImagesMetadata = 'images_metadata';
$db_local_dbImagesPhotoselects = 'images_photoselects_jpg';
//$db_local_dbImagesRetouched = 'images_retouched_jpg';
//$db_local_dbUploadPrimary = 'upload_primary_jpg-png';
//$db_local_dbUploadAlt = 'upload_alt_jpg-png';

///--Primary Database and Table Variables--Set in each specific script
$db_local_database  =   $db_local_dbImagesPhotoselects;
//$db_local_table     =   $db_local_tblImages;
//Connect to MySQL Server 



$db = mysql_connect($db_local_hostname, $db_local_username, $db_local_password);
if (!$db) {
echo "Unable to establish connection to database server";
exit;
}

if (!mysql_select_db($db_local_database, $db)) {
echo "Unable to connect to database";
exit;
}
?>
