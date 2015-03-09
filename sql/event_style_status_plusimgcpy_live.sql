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
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID        AS "colorstyle",
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID                AS "event_id",
  POMGR.EVENT.EVENT_DESCRIPTION                     AS "event_title",
  POMGR.EVENT_GROUP.NAME                            AS "event_group",
  POMGR.EVENT.DESCRIPTION                           AS "event_description",
  POMGR.EVENT.NAME                                  AS "event_detail",
  POMGR.EVENT.DURATION                              AS "event_duration",
  to_date(POMGR.EVENT.START_DATE, 'YYYY-MM-DD')     AS "ev_start",
  to_date(POMGR.EVENT.END_DATE, 'YYYY-MM-DD')       AS "ev_end",
  POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME              AS "product_category",
  POMGR.LK_PRODUCT_STATUS.NAME                    AS "production_status",
  to_date(POMGR.PRODUCT_COLOR.IMAGE_READY_DT, 'YYYY-MM-DD')               AS "image_dt",
  to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')                AS "copy_dt",
  to_date(POMGR.EVENT.SHOT_LIST_DATE, 'YYYY-MM-DD') AS "studio_dt",
  POMGR.LK_EVENT_TYPE.NAME                          AS "event_type",
  POMGR.LK_EVENT_SOURCE.NAME                        AS "event_source"
FROM
  POMGR.EVENT_PRODUCT_COLOR
LEFT JOIN POMGR.EVENT
ON
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = POMGR.EVENT.ID
LEFT JOIN POMGR.EVENT_GROUP
ON
  POMGR.EVENT.GROUP_ID = POMGR.EVENT_GROUP.ID
LEFT JOIN POMGR.LK_EVENT_TYPE
ON
  POMGR.EVENT.STATUS = POMGR.LK_EVENT_TYPE.ID
LEFT JOIN POMGR.LK_EVENT_SOURCE
ON
  POMGR.EVENT.STATUS = POMGR.LK_EVENT_SOURCE.ID
LEFT JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
ON
  POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
LEFT JOIN POMGR.PRODUCT_COLOR
ON
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
LEFT JOIN POMGR.LK_PRODUCT_STATUS
ON
  POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
WHERE
  POMGR.EVENT_GROUP.NAME != 'test'
ORDER BY
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID DESC;
  
  
  
spool off
exit;
