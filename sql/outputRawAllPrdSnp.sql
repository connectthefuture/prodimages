set echo off
set verify off
set termout on
-- set heading off
set headsep off
set null "null"
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
set trimspool off
set newpage none
set linesize 7500
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/outputRawAllPrdSnpSpool.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "Style_Number",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND AS "Brand_Name",
  ATG_SNP.EVENT_GROUP.NAME  AS "Event_Group_Name",
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY AS "Copy_Ready_Date",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME AS "Product_Type",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS AS "Production_Status",
  ATG_SNP.EVENT_GROUP.ID  AS "Event_Group_ID",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS AS "Sample_Status",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE AS "Sample_Date",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME AS "Department",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME AS "Gender"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((sysdate) - 90);
ORDER by  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE desc;
spool off;
exit;
--Style_Number,Brand_Name,Event_Group_Namem,Copy_Ready_Date,Product_Type,Production_Status,Event_Group_ID,Sample_Status,Sample_Date,Department,Gender
