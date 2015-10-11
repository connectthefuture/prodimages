-- #!/usr/local/oracle/instantclient10_1/sqlplus

--jbragato/'Blu3f!y'@//192.168.30.66:1531/dssprd1
-- spoolCsv="/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/exiftoolMetaData.csv"
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
-- spool /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/exiftoolCsvMetaData.csv
-- cat exiftoolMetaData.csv | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g > ~/exifFixed.csv



SELECT /* PrdExtra_CSV_UPDATES39437d */  /* CSV_UPDATES63b89a */  DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE        AS "SourceFile",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND             AS "XMP:Artist",
  ATG_SNP.EVENT_GROUP.NAME                     AS "XMP:Album",
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY        AS "IPTC:SpecialInstructions",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME       AS "XMP:Genre",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS AS "IPTC:CopyrightNotice",
  ATG_SNP.EVENT_GROUP.ID                       AS "IPTC:Credit",
  ATG_SNP.SAMPLE_TRACKING.SAMPLE_ID            AS "XMP:Source"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
LEFT JOIN ATG_SNP.SHP_HDR Vendor_Ship_Status
ON
  Vendor_Ship_Status.PO_HDR_ID = POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR
LEFT JOIN ATG_SNP.SHP_SKU
ON
  ATG_SNP.SHP_SKU.SHP_HDR_ID = Vendor_Ship_Status.ID
LEFT JOIN ATG_SNP.SAMPLE_TRACKING
ON
  ATG_SNP.SHP_SKU.PO_SKU_ID = ATG_SNP.SAMPLE_TRACKING.ID
LEFT JOIN POMGR_SNP.SAMPLE_TRACKING_NUMBER
ON
  ATG_SNP.SAMPLE_TRACKING.STATUS_ID =
  POMGR_SNP.SAMPLE_TRACKING_NUMBER.SAMPLE_ID
LEFT JOIN POMGR_SNP.TRACKING_NUMBER
ON
  POMGR_SNP.SAMPLE_TRACKING_NUMBER.SAMPLE_ID = POMGR_SNP.TRACKING_NUMBER.ID
WHERE INACTIVE_REASON IS NULL
-- AND PRODUCTION_STATUS = 'Production Incomplete'
AND SAMPLE_STATUS != 'Pending Sample'
AND SAMPLE_STATUS != 'Sample Sent to Bluefly'
-- AND SAMPLE_STATUS != 'Sample Sent to Warehouse'
-- AND SAMPLE_STATUS != 'Scanned Out to Warehouse' 
-- AND SAMPLE_STATUS != 'Pending Sent to Warehouse'
AND SAMPLE_STATUS != 'Sample Sent to Buyers';
-- POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_COMPLETE_DT IS NULL;
-- spool off;
exit;
