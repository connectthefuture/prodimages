set echo off
set verify off
set termout on
-- set heading off
-- set headsep ","
-- set markup html on
set pagesize 49500
set colsep "__"
-- set recsep ";"
set pages 49500
set feedback off
set trimspool on
set newpage none
set linesize 32000
set null "NULL"
-- set wrap off
-- SET MARKUP HTML ON SPOOL ON
-- set space 1
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spool_eventcolorstylesplus.csv

SELECT DISTINCT
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID        AS "colorstyle",
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID                AS "event_id",
  ATG_SNP.EVENT.EVENT_DESCRIPTION                     AS "event_title",
  ATG_SNP.EVENT_GROUP.NAME                            AS "event_group",
  ATG_SNP.EVENT.DESCRIPTION                           AS "event_description",
  ATG_SNP.EVENT.NAME                                  AS "event_detail",
  ATG_SNP.EVENT.DURATION                              AS "event_duration",
  to_date(ATG_SNP.EVENT.START_DATE, 'YYYY-MM-DD')     AS "ev_start",
  to_date(ATG_SNP.EVENT.END_DATE, 'YYYY-MM-DD')       AS "ev_end",
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME              AS "product_category",
  POMGR_SNP.LK_PRODUCT_STATUS.NAME                    AS "production_status",
  to_date(POMGR_SNP.PRODUCT_COLOR.IMAGE_READY_DT, 'YYYY-MM-DD')               AS "image_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')                AS "copy_dt",
  to_date(ATG_SNP.EVENT.SHOT_LIST_DATE, 'YYYY-MM-DD') AS "studio_dt",
  ATG_SNP.LK_EVENT_TYPE.NAME                          AS "event_type",
  ATG_SNP.LK_EVENT_SOURCE.NAME                        AS "event_source"
FROM
  ATG_SNP.EVENT_PRODUCT_COLOR
LEFT JOIN ATG_SNP.EVENT
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT.GROUP_ID = ATG_SNP.EVENT_GROUP.ID
LEFT JOIN ATG_SNP.LK_EVENT_TYPE
ON
  ATG_SNP.EVENT.STATUS = ATG_SNP.LK_EVENT_TYPE.ID
LEFT JOIN ATG_SNP.LK_EVENT_SOURCE
ON
  ATG_SNP.EVENT.STATUS = ATG_SNP.LK_EVENT_SOURCE.ID
LEFT JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY
ON
  ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID
LEFT JOIN POMGR_SNP.PRODUCT_COLOR
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR_SNP.PRODUCT_COLOR.ID
LEFT JOIN POMGR_SNP.LK_PRODUCT_STATUS
ON
  POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
WHERE
  ATG_SNP.EVENT_GROUP.NAME != 'test'
ORDER BY
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID DESC,
  ATG_SNP.EVENT_GROUP.NAME DESC;
  
  
  
spool off
exit;
