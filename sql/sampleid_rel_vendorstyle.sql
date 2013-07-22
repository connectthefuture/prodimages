set echo off
set verify off
set termout on
set array 3000                      
--set heading on
--set headsep ","
set pagesize 50000
set colsep "||"
set pages 50000
set feedback off
--set tab on
set trimspool on
--set recsep "|"
--set trimout on
set null "-"
set newpage none
set linesize 5000
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolGeneralimport.csv

SELECT
  POMGR_SNP.PRODUCT_COLOR.ID                                      AS "colorstyle",
  POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE                            AS "vendor_style",
  POMGR_SNP.SKU.SKU_CODE                                          AS "sku",
  POMGR_SNP."SAMPLE".ID                                           AS "sample_id",
  MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS "sample_date",
  POMGR_SNP.LK_SAMPLE_STATUS.NAME                                 AS "sample_status",
  POMGR_SNP.LK_SAMPLE_LOCATION.NAME                               AS "sample_location",
  POMGR_SNP.VENDOR_SIZE_VALUE.NAME                                AS "sample_size",
  POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID                          AS "color_group_id",
  POMGR_SNP.PRODUCT_COLOR.VENDOR_COLOR                            AS "vendor_color"
FROM
  POMGR_SNP."SAMPLE"
INNER JOIN POMGR_SNP.LK_SAMPLE_STATUS
ON
  POMGR_SNP."SAMPLE".STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID
INNER JOIN POMGR_SNP.LK_SAMPLE_LOCATION
ON
  POMGR_SNP.LK_SAMPLE_STATUS.LOCATION_ID = POMGR_SNP.LK_SAMPLE_LOCATION.ID
INNER JOIN POMGR_SNP.PRODUCT_COLOR
ON
  POMGR_SNP."SAMPLE".PRODUCT_COLOR_ID = POMGR_SNP.PRODUCT_COLOR.ID
INNER JOIN POMGR_SNP.SKU
ON
  POMGR_SNP."SAMPLE".SKU_ID = POMGR_SNP.SKU.ID
RIGHT JOIN POMGR_SNP.VENDOR_SIZE_VALUE
ON
  POMGR_SNP.SKU.VENDOR_SIZE_VALUE_ID = POMGR_SNP.VENDOR_SIZE_VALUE.ID
RIGHT JOIN POMGR_SNP.SAMPLE_TRACKING
ON
  POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID = POMGR_SNP."SAMPLE".ID
WHERE
  POMGR_SNP.PRODUCT_COLOR.ID               IS NOT NULL
AND POMGR_SNP.VENDOR_SIZE_VALUE.SAMPLE_SIZE = '1'
GROUP BY
  POMGR_SNP.PRODUCT_COLOR.ID,
  POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE,
  POMGR_SNP.SKU.SKU_CODE,
  POMGR_SNP."SAMPLE".ID,
  POMGR_SNP.LK_SAMPLE_STATUS.NAME,
  POMGR_SNP.LK_SAMPLE_LOCATION.NAME,
  POMGR_SNP.VENDOR_SIZE_VALUE.SAMPLE_SIZE,
  POMGR_SNP.VENDOR_SIZE_VALUE.NAME,
  POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID,
  POMGR_SNP.PRODUCT_COLOR.VENDOR_COLOR 
ORDER BY
  POMGR_SNP.PRODUCT_COLOR.ID DESC,
  POMGR_SNP.SKU.SKU_CODE DESC;
  
spool off
exit;
