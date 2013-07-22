set echo off
set verify off
set termout on
-- set heading off
set headsep off
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
set trimspool on
set newpage none
set linesize 5000
spool /mnt/Post_Ready/zProd_Primary/imageServer/tmp/limbo/spoolDWImport.csv

SELECT /* PrdExtra_CSV_UPDATESf8fecf */  /* CSV_UPDATESba1bb5 */  DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "ColorStyle"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
WHERE INACTIVE_REASON IS NULL
AND MAIN_IMAGE = 'N'
AND ZOOM_IMAGE = 'N'
AND IMAGE_READY IS NULL
AND PRODUCTION_STATUS = 'Production Incomplete'
AND SAMPLE_STATUS != 'Pending Sample'
AND SAMPLE_STATUS != 'Sample Sent to Bluefly'
AND SAMPLE_STATUS != 'Sample Sent to Warehouse'
AND SAMPLE_STATUS != 'Scanned Out to Warehouse' 
AND SAMPLE_STATUS != 'Pending Sent to Warehouse'
AND SAMPLE_STATUS != 'Sample Sent to Buyers';
spool off;
exit;
