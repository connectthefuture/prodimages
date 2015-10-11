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
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID                AS "colorstyle",
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID                        AS "event_id",
  ATG_SNP.EVENT.EVENT_DESCRIPTION                             AS "event_title",
  ATG_SNP.EVENT_GROUP.NAME                                    AS "event_group",
  ATG_SNP.EVENT.DESCRIPTION                                   AS "event_description",
  ATG_SNP.EVENT.NAME                                          AS "event_detail",
  ATG_SNP.EVENT.STATUS                                        AS "event_status",
  ATG_SNP.EVENT.DURATION                                      AS "event_duration",
  to_date(ATG_SNP.EVENT.START_DATE, 'YYYY-MM-DD')             AS "ev_start",
  to_date(ATG_SNP.EVENT.END_DATE, 'YYYY-MM-DD')               AS "ev_end",
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME                      AS "product_category",
  ATG_SNP.LK_EVENT_TYPE.NAME                                  AS "event_type",
  ATG_SNP.LK_EVENT_SOURCE.NAME                                AS "event_source",
  to_date(ATG_SNP.EVENT.SHOT_LIST_DATE, 'YYYY-MM-DD')         AS "studio_dt",
  --ATG_SNP.EVENT.FEATURE_STYLES                                AS "feature_info",
  ATG_SNP.EVENT.CATEGORY                                      AS "jda_cat"
FROM
  ATG_SNP.EVENT_PRODUCT_COLOR
LEFT JOIN ATG_SNP.EVENT
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID
INNER JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT.GROUP_ID = ATG_SNP.EVENT_GROUP.ID
INNER JOIN ATG_SNP.LK_EVENT_TYPE
ON
  ATG_SNP.EVENT.STATUS = ATG_SNP.LK_EVENT_TYPE.ID
INNER JOIN ATG_SNP.LK_EVENT_SOURCE
ON
  ATG_SNP.EVENT.STATUS = ATG_SNP.LK_EVENT_SOURCE.ID
INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY
ON
  ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID
WHERE
  ATG_SNP.EVENT.START_DATE >= TRUNC((SysDate) - 60)
AND
  ATG_SNP.EVENT_GROUP.NAME != 'test'
ORDER BY
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID DESC,
  ATG_SNP.EVENT_GROUP.NAME DESC;
  
  spool off
exit;
