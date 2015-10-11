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
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spool_eventcolorstyles.csv

SELECT
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID                AS "colorstyle",
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID                        AS "event_id",
  POMGR.EVENT.EVENT_DESCRIPTION                             AS "event_title",
  POMGR.EVENT_GROUP.NAME                                    AS "event_group",
  POMGR.EVENT.DESCRIPTION                                   AS "event_description",
  POMGR.EVENT.NAME                                          AS "event_detail",
  POMGR.EVENT.STATUS                                        AS "event_status",
  POMGR.EVENT.DURATION                                      AS "event_duration",
  to_date(POMGR.EVENT.START_DATE, 'YYYY-MM-DD')             AS "ev_start",
  to_date(POMGR.EVENT.END_DATE, 'YYYY-MM-DD')               AS "ev_end",
  POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME                      AS "product_category",
  POMGR.LK_EVENT_TYPE.NAME                                  AS "event_type",
  POMGR.LK_EVENT_SOURCE.NAME                                AS "event_source",
  to_date(POMGR.EVENT.SHOT_LIST_DATE, 'YYYY-MM-DD')         AS "studio_dt",
  --POMGR.EVENT.FEATURE_STYLES                                AS "feature_info",
  POMGR.EVENT.CATEGORY                                      AS "jda_cat"
FROM
  POMGR.EVENT_PRODUCT_COLOR
LEFT JOIN POMGR.EVENT
ON
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = POMGR.EVENT.ID
INNER JOIN POMGR.EVENT_GROUP
ON
  POMGR.EVENT.GROUP_ID = POMGR.EVENT_GROUP.ID
INNER JOIN POMGR.LK_EVENT_TYPE
ON
  POMGR.EVENT.STATUS = POMGR.LK_EVENT_TYPE.ID
INNER JOIN POMGR.LK_EVENT_SOURCE
ON
  POMGR.EVENT.STATUS = POMGR.LK_EVENT_SOURCE.ID
INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
ON
  POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
WHERE
  POMGR.EVENT.START_DATE >= TRUNC((SysDate) - 60)
AND
  POMGR.EVENT_GROUP.NAME != 'test'
ORDER BY
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID DESC,
  POMGR.EVENT_GROUP.NAME DESC;
  
  spool off
exit;
