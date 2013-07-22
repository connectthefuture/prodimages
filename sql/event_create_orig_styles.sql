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


SELECT DISTINCT
  ATG_SNP.EVENT.ID                                             AS "event_id",
  POMGR_SNP.LK_GENDER.CODE                                     AS "gender",
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME                       AS "category",
  ATG_SNP.EVENT.EVENT_DESCRIPTION                              AS "event_title",
  ATG_SNP.EVENT.START_DATE                                     AS "ev_start",
  ATG_SNP.EVENT.CREATED_DATE                                   AS "cdate",
  USERS1.USERNAME                                              AS "createdby",
  ATG_SNP.EVENT.MODIFIED_DATE                                  AS "moddate",
  ATG_SNP.USERS.USERNAME                                       AS "modifiedby",
  ATG_SNP.EVENT.STATUS                                         AS "event_status",
  COUNT(DISTINCT ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID) AS "style_ct",
  ATG_SNP.EVENT.DURATION                                       AS "duration",
  ATG_SNP.EVENT.DESCRIPTION                                    AS "full_desc"
FROM
  ATG_SNP.EVENT
LEFT JOIN ATG_SNP.USERS
ON
  ATG_SNP.EVENT.MODIFIED_BY = ATG_SNP.USERS.ID
LEFT JOIN ATG_SNP.USERS USERS1
ON
  ATG_SNP.EVENT.CREATED_BY = USERS1.ID
LEFT JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY
ON
  ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID
LEFT JOIN POMGR_SNP.LK_GENDER
ON
  ATG_SNP.EVENT.GENDER_ID = POMGR_SNP.LK_GENDER.ID
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR
ON
  ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID,
  POMGR_SNP.CATEGORY_DENORMALIZED
WHERE
  ATG_SNP.EVENT.CREATED_DATE >= TRUNC(SysDate - 10)
GROUP BY
  ATG_SNP.EVENT.ID,
  POMGR_SNP.LK_GENDER.CODE,
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME,
  ATG_SNP.EVENT.EVENT_DESCRIPTION,
  ATG_SNP.EVENT.START_DATE,
  ATG_SNP.EVENT.CREATED_DATE,
  USERS1.USERNAME,
  ATG_SNP.EVENT.MODIFIED_DATE,
  ATG_SNP.USERS.USERNAME,
  ATG_SNP.EVENT.STATUS,
  ATG_SNP.EVENT.DURATION,
  ATG_SNP.EVENT.DESCRIPTION
ORDER BY
  ATG_SNP.EVENT.ID DESC
  
spool off

exit;

