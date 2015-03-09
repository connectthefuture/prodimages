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
set linesize 20000
-- spool /mnt/Post_Ready/zProd_Primary/imageServer/tmp/limbo/spoolDWImport.csv

SELECT /* PrdExtra_CSV_UPDATESb9cf72 */  /* CSV_UPDATESdfc9d6 */  DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "ColorStyle"
--	POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS AS "Sample_Status",
--	POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE AS "Status_Date"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
-- WHERE INACTIVE_REASON IS NULL
-- AND MAIN_IMAGE = 'N'
-- AND 
WHERE POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((SysDate) - 60)
AND ZOOM_IMAGE = 'N'
AND IMAGE_READY IS NULL
-- AND PRODUCTION_STATUS = 'Production Incomplete'
-- AND SAMPLE_STATUS != 'Pending Sample'
AND SAMPLE_STATUS != 'Sample Sent to Bluefly';
-- AND SAMPLE_STATUS != 'Sample Sent to Warehouse'
-- AND SAMPLE_STATUS != 'Scanned Out to Warehouse' 
-- AND SAMPLE_STATUS != 'Pending Sent to Warehouse'
-- AND SAMPLE_STATUS != 'Sample Sent to Buyers';
-- spool off;
exit;
