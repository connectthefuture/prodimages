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
set linesize 31500
-- spool /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/spoolexiftoolCsvMetaData.csv
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolexiftoolCsvMetaData.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE        AS "SourceFile",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND             AS "Keywords",
  ATG_SNP.EVENT_GROUP.NAME                     AS "XMP:Album",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY, 'YYYY-MM-DD')        AS "IPTC:SpecialInstructions",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME       AS "XMP:Genre",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS AS "IPTC:CopyrightNotice",
  MAX(ATG_SNP.EVENT_GROUP.ID)                  AS "IPTC:Credit",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS     AS "IPTC:Source",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE, 'YYYY-MM-DD')  AS "IPTC:SimilarityIndex"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
--LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
INNER JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
INNER JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= trunc((sysdate) - 40)
GROUP BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  ATG_SNP.EVENT_GROUP.NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE
ORDER BY
   POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC;
spool off
exit;
