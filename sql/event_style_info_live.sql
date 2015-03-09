set echo off
set verify off
set termout on
-- set heading off
-- set headsep ","
-- set markup html on
set pagesize 49500
set colsep ","
-- set recsepchar ";"
set pages 49500
set feedback off
set trimspool on
set newpage none
set linesize 32000
-- set space 1
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spool_eventsnapshot.csv

SELECT
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID                            AS "colorstyle",
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID                                    AS "event_id",
  POMGR.EVENT.STATUS                                                    AS "event_deploy_status",
  POMGR.LK_EVENT_TYPE.NAME                                              AS "event_type",
  POMGR.EVENT_GROUP.NAME                                                AS "bc_event_name",
  to_date(POMGR.EVENT.START_DATE, 'YYYY-MM-DD')                         AS "event_start_dt",
  to_date(POMGR.EVENT.END_DATE, 'YYYY-MM-DD')                           AS "event_end_dt",
  POMGR.LK_EVENT_SOURCE.NAME                                            AS "bc_event_source",
  POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME                                  AS "atg_prd_category",
  POMGR.LK_PRODUCT_STATUS.NAME                                        AS "production_status",
  to_date(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD')   AS "production_complete_dt",
  to_date(POMGR.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE, 'YYYY-MM-DD') AS "pmshot_dt",
  to_date(POMGR.PRODUCT_COLOR.IMAGE_READY_DT, 'YYYY-MM-DD')           AS "image_ready_dt",
  to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')            AS "copy_ready_dt"
FROM
  POMGR.EVENT_PRODUCT_COLOR
INNER JOIN POMGR.EVENT
ON
  POMGR.EVENT.ID = POMGR.EVENT_PRODUCT_COLOR.EVENT_ID
INNER JOIN POMGR.LK_EVENT_TYPE
ON
  POMGR.EVENT.TYPE_ID = POMGR.LK_EVENT_TYPE.ID
INNER JOIN POMGR.EVENT_GROUP
ON
  POMGR.EVENT_GROUP.ID = POMGR.EVENT.GROUP_ID
INNER JOIN POMGR.PRODUCT_COLOR_DETAIL
ON
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID
INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
ON
  POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
INNER JOIN POMGR.LK_EVENT_SOURCE
ON
  POMGR.EVENT.SOURCE_ID = POMGR.LK_EVENT_SOURCE.ID
INNER JOIN POMGR.PRODUCT_COLOR
ON
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
INNER JOIN POMGR.LK_PRODUCT_STATUS
ON
  POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
ORDER BY
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID;
  
spool off
exit;


