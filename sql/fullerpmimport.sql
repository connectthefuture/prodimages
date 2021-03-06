set echo off
set verify off
set termout on
set array 3000                      
--set heading on
set headsep "|"
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
--set tab on
set trimspool off
--set recsep "|"
--set trimout on
set null "-"
set newpage none
set linesize 5000
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolDWMerchantTags.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE                                   AS "colorstyle",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND                                        AS "Keywords",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS                            AS "IPTC:CopyrightNotice",
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR                                       AS "IPTC:PONumber",
  POMGR_SNP.USERS.USERNAME                                                AS "IPTC:MerchantName",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS                                AS "IPTC:Source",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,'YYYY-MM-DD')     AS "IPTC:SampleStatusDate",
  SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND)                       AS "IPTC:SampleInventory",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,'YYYY-MM-DD')             AS "COPY_READY",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY,'YYYY-MM-DD')            AS "IMAGE_READY",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE,'YYYY-MM-DD')             AS "START_DATE",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_COMPLETE_DT,'YYYY-MM-DD') AS "PRODUCTION_COMPLETE_DT",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.ORIGINAL_START_DATE,'YYYY-MM-DD')    AS "ORIGINAL_START_DATE",
  POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_SIZE_CHART                            AS "Vendor_Size_Chart",
  POMGR_SNP.PRODUCT_SNAPSHOT.COLOR_GROUP                                  AS "Color"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
INNER JOIN POMGR_SNP.PO_HDR
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = POMGR_SNP.PO_HDR.ID
INNER JOIN POMGR_SNP.USERS
ON
  POMGR_SNP.USERS.ID = POMGR_SNP.PO_HDR.USER_ID
WHERE
  (
    POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((SysDate) - 30)
    AND POMGR_SNP.PRODUCT_SNAPSHOT.INACTIVE_REASON  IS NULL
    AND POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Scanned In at Bluefly'
  )
OR
  (
    POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((SysDate) - 30)
    AND POMGR_SNP.PRODUCT_SNAPSHOT.INACTIVE_REASON  IS NULL
    AND POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Sample Sent to Bluefly'
  )
OR
  (
    POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Scanned Out to Buyers'
  )
GROUP BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR,
  POMGR_SNP.USERS.USERNAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,
  POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY,
  POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_COMPLETE_DT,
  POMGR_SNP.PRODUCT_SNAPSHOT.ORIGINAL_START_DATE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_SIZE_CHART,
  POMGR_SNP.PRODUCT_SNAPSHOT.COLOR_GROUP
HAVING
  SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) >= 0
ORDER BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC Nulls Last;
spool off
exit;
