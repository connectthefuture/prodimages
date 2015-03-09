set echo off
set verify off
set termout on
set array 4000    
set wrap off
--set heading on
--set headsep "|"
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
--set tab on
set trimspool on
--set recsep "|"
--set trimout on
set null "-"
set newpage none
set linesize 32766
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolpmaimportprodsnapshot.csv

SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE                                   AS "colorstyle",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND                                        AS "brand",
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS                            AS "production_status",
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR                                       AS "po_number",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS                                AS "sample_status",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,'YYYY-MM-DD')     AS "status_dt",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,'YYYY-MM-DD')             AS "copy_ready_dt",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY,'YYYY-MM-DD')            AS "image_ready_dt",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_COMPLETE_DT,'YYYY-MM-DD') AS "production_complete_dt",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE,'YYYY-MM-DD')             AS "start_dt",
  to_date(POMGR_SNP.PRODUCT_SNAPSHOT.ORIGINAL_START_DATE,'YYYY-MM-DD')    AS "orig_start_dt",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME                                  AS "gender",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME                                  AS "category",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME                                  AS "product_type",
  POMGR_SNP.PRODUCT_SNAPSHOT.PHOTOGRAPHED_DATE                            AS "sample_image_dt",
  POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO                              AS "vendor_style",
  POMGR_SNP.PRODUCT_SNAPSHOT.COLOR_GROUP                                  AS "color"
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
INNER JOIN POMGR_SNP.PO_HDR
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = POMGR_SNP.PO_HDR.ID
INNER JOIN POMGR_SNP.USERS
ON
  POMGR_SNP.USERS.ID = POMGR_SNP.PO_HDR.USER_ID
WHERE
  (
    POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= TRUNC((SysDate) - 550)
  )
ORDER BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC Nulls Last;
spool off
exit;
