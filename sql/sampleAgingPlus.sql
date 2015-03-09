set echo off
set verify off
set termout on
-- set heading off
--set headsep ","
--set markup html on
set pagesize 49500
set colsep ",,"
set recsepchar ";"
set pages 49500
set feedback off
set trimspool on
set newpage none
set linesize 32000
--set space 1
-- spool /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/spoolexiftoolCsvMetaData.csv
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spool_sampleAging.csv

SELECT
  POMGR_SNP.PRODUCT_COLOR.ID                                                        AS "colorstyle",
  POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE                                              AS "vendor_style",
  POMGR_SNP.SKU.SKU_CODE                                                            AS "sku",
  POMGR_SNP."SAMPLE".ID                                                             AS "sample_id",
  MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD'))                   AS "sample_dt",
  POMGR_SNP.LK_SAMPLE_STATUS.NAME                                                   AS "sample_status",
  POMGR_SNP.LK_SAMPLE_LOCATION.NAME                                                 AS "sample_location",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE                                     AS "status_dt",
  POMGR_SNP.VENDOR_SIZE_VALUE.NAME                                                  AS "sample_size",
  POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID                                            AS "color_group_id",
  POMGR_SNP.PRODUCT_COLOR.VENDOR_COLOR                                              AS "vendor_color",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND                                                  AS "brand",
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND_TYPE                                             AS "brand_type",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME                                            AS "gender",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME                                            AS "category",
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME                                            AS "product_type",
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_IMAGE                                           AS "sample_image"
FROM
  POMGR_SNP."SAMPLE"
INNER JOIN POMGR_SNP.LK_SAMPLE_STATUS
ON
  POMGR_SNP."SAMPLE".STATUS_ID              =   POMGR_SNP.LK_SAMPLE_STATUS.ID
INNER JOIN POMGR_SNP.LK_SAMPLE_LOCATION
ON
  POMGR_SNP.LK_SAMPLE_STATUS.LOCATION_ID    =   POMGR_SNP.LK_SAMPLE_LOCATION.ID
INNER JOIN POMGR_SNP.PRODUCT_COLOR
ON
  POMGR_SNP."SAMPLE".PRODUCT_COLOR_ID       =   POMGR_SNP.PRODUCT_COLOR.ID
INNER JOIN POMGR_SNP.SKU
ON
  POMGR_SNP."SAMPLE".SKU_ID                 =   POMGR_SNP.SKU.ID
RIGHT JOIN POMGR_SNP.VENDOR_SIZE_VALUE
ON
  POMGR_SNP.SKU.VENDOR_SIZE_VALUE_ID        =   POMGR_SNP.VENDOR_SIZE_VALUE.ID
RIGHT JOIN POMGR_SNP.SAMPLE_TRACKING
ON
  POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID       =   POMGR_SNP."SAMPLE".ID
INNER JOIN POMGR_SNP.PRODUCT_SNAPSHOT
ON
  POMGR_SNP.PRODUCT_COLOR.ID                =   POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE
WHERE
  (
  POMGR_SNP.PRODUCT_COLOR.ID                      IS NOT NULL
  AND 
  POMGR_SNP.VENDOR_SIZE_VALUE.SAMPLE_SIZE         = '1'
  AND 
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE   >= TRUNC((SysDate) - 5)
  )
GROUP BY
  POMGR_SNP.PRODUCT_COLOR.ID,
  POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE,
  POMGR_SNP.SKU.SKU_CODE,
  POMGR_SNP."SAMPLE".ID,
  POMGR_SNP.LK_SAMPLE_STATUS.NAME,
  POMGR_SNP.LK_SAMPLE_LOCATION.NAME,
  POMGR_SNP.VENDOR_SIZE_VALUE.NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,
  POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID,
  POMGR_SNP.PRODUCT_COLOR.VENDOR_COLOR,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND_TYPE,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_IMAGE,
  POMGR_SNP.VENDOR_SIZE_VALUE.SAMPLE_SIZE,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME
ORDER BY
  POMGR_SNP.PRODUCT_COLOR.ID DESC,
  POMGR_SNP.SKU.SKU_CODE DESC;
  spool off
  exit;
