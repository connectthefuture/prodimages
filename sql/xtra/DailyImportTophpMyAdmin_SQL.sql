set echo off
set verify off
set termout on
set array 3000                      
-- set heading on
set headsep off
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
--set tab on
set trimspool on
-- recsep 
--set trimout on
set null "-"
set newpage none
set linesize 8000
-- spool /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/spoolexiftoolCsvMetaData.csv
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolphpmyAdminClean.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "Style_Number",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND AS "Brand_Name",
  ATG_SNP.EVENT_GROUP.NAME  AS "Event_Group_Name",
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY AS "Copy_Ready_Date",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME AS "Product_Type",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS AS "Production_Status",
  ATG_SNP.EVENT_GROUP.ID  AS "Event_Group_ID",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS AS "Sample_Status",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE AS "IPTC:SampleStatusDate",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME AS "IPTC:Department",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME AS "IPTC:Gender"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((sysdate) - 30);
spool off
exit;
