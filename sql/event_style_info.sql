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
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID                            AS "colorstyle",
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID                                    AS "event_id",
  ATG_SNP.EVENT.STATUS                                                    AS "event_deploy_status",
  ATG_SNP.LK_EVENT_TYPE.NAME                                              AS "event_type",
  ATG_SNP.EVENT_GROUP.NAME                                                AS "bc_event_name",
  to_date(ATG_SNP.EVENT.START_DATE, 'YYYY-MM-DD')                         AS "event_start_dt",
  to_date(ATG_SNP.EVENT.END_DATE, 'YYYY-MM-DD')                           AS "event_end_dt",
  ATG_SNP.LK_EVENT_SOURCE.NAME                                            AS "bc_event_source",
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME                                  AS "atg_prd_category",
  POMGR_SNP.LK_PRODUCT_STATUS.NAME                                        AS "production_status",
  to_date(POMGR_SNP.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD')   AS "production_complete_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE, 'YYYY-MM-DD') AS "pmshot_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR.IMAGE_READY_DT, 'YYYY-MM-DD')           AS "image_ready_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')            AS "copy_ready_dt"
FROM
  ATG_SNP.EVENT_PRODUCT_COLOR
INNER JOIN ATG_SNP.EVENT
ON
  ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID
INNER JOIN ATG_SNP.LK_EVENT_TYPE
ON
  ATG_SNP.EVENT.TYPE_ID = ATG_SNP.LK_EVENT_TYPE.ID
INNER JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = ATG_SNP.EVENT.GROUP_ID
INNER JOIN POMGR_SNP.PRODUCT_COLOR_DETAIL
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR_SNP.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID
INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY
ON
  ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID
INNER JOIN ATG_SNP.LK_EVENT_SOURCE
ON
  ATG_SNP.EVENT.SOURCE_ID = ATG_SNP.LK_EVENT_SOURCE.ID
INNER JOIN POMGR_SNP.PRODUCT_COLOR
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR_SNP.PRODUCT_COLOR.ID
INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS
ON
  POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
ORDER BY
  ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID;
  
spool off
exit;


