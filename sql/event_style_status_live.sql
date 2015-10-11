set echo off
set verify off
set termout on
set array 4000    
set wrap off
--set heading on
--set headsep "|"
set pagesize 50000
set colsep "__"
set pages 50000
set feedback off
--set tab on
set trimspool on
--set recsep "|"
--set trimout on
set null "-"
set newpage none
set linesize 32766
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spooleventstylestatus.csv

SELECT
  POMGR.PRODUCT_COLOR.ID                                                AS "colorstyle",
  POMGR.LK_PRODUCT_STATUS.NAME                                          AS "production_status",
  to_date(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD')     AS "production_complete_dt",
  to_date(POMGR.PRODUCT_COLOR.MODIFIED_DATE, 'YYYY-MM-DD')              AS "modify_dt",
  POMGR.PRODUCT_COLOR.VENDOR_STYLE                                      AS "vendor_style",
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID                                      AS "event_id"
FROM
  POMGR.PRODUCT_COLOR
INNER JOIN POMGR.EVENT_PRODUCT_COLOR
ON
  POMGR.PRODUCT_COLOR.ID = POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID
INNER JOIN POMGR.LK_PRODUCT_STATUS
ON
  POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
ORDER BY
  POMGR.EVENT_PRODUCT_COLOR.EVENT_ID DESC,
  POMGR.LK_PRODUCT_STATUS.NAME ASC;

spool off
exit;
