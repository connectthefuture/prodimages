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
set linesize 5000
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolDWInitialStaticTags.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE             AS "SourceFile",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND                  AS "Keywords",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME            AS "IPTC:Gender",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME            AS "XMP:Genre",
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR                 AS "IPTC:PONumber",
  POMGR_SNP.USERS.USERNAME                          AS "IPTC:MerchantName"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
INNER JOIN POMGR_SNP.PO_HDR
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = POMGR_SNP.PO_HDR.ID
INNER JOIN POMGR_SNP.USERS
ON
  POMGR_SNP.USERS.ID = POMGR_SNP.PO_HDR.USER_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((sysdate) - 18)
AND 
  POMGR_SNP.PRODUCT_SNAPSHOT.INACTIVE_REASON  IS NULL
AND 
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Scanned In at Bluefly'
OR  
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Sample Sent to Bluefly'
OR  
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS = 'Scanned Out to Buyers'
GROUP BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR,
  POMGR_SNP.USERS.USERNAME
ORDER BY
   POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC;
spool off
exit;