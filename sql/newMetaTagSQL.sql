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
-- spool /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/spoolexiftoolCsvMetaData.csv
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/exifFixed.csv

SELECT /* PrdExtra_CSV_UPDATES4b96c6 */  /* CSV_UPDATESdc7478 */  DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE                               AS "SourceFile",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND                                    AS "XMP:Artist",
  ATG_SNP.EVENT_GROUP.NAME                                            AS "XMP:Album",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE, 'YYYY-MM-DD')        AS "IPTC:SpecialInstructions",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME                              AS "XMP:Genre",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS                        AS "IPTC:CopyrightNotice",
  ATG_SNP.EVENT_GROUP.ID                                              AS "IPTC:Credit",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS                            AS "IPTC:Source"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS  = 'Production Incomplete'
  AND POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS   != 'Pending Sample'
  AND POMGR_SNP.PRODUCT_SNAPSHOT.INACTIVE_REASON IS NULL
OR
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS != 'Sample Sent to Bluefly'
GROUP BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  ATG_SNP.EVENT_GROUP.NAME,
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE, 'YYYY-MM-DD'),
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS,
  ATG_SNP.EVENT_GROUP.ID,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS
HAVING
  SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) > 0
ORDER BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC Nulls Last;
spool off
exit;
