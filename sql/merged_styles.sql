set echo off
set verify off
set termout off
set array 3000                      
--set heading on
--set headsep ","
set pagesize 50000
set colsep ","
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
  POMGR_SNP.ADT_COLORSTYLE_MERGE.TRG_PRODUCTCOLOR_ID                        AS "current_style",
  POMGR_SNP.ADT_COLORSTYLE_MERGE.SRC_PRODUCTCOLOR_ID                        AS "voided_style",
  to_date(POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE, 'YYYY-MM-DD')       AS "merge_date",
  POMGR_SNP.USERS.USERNAME                                                  AS "username"
FROM
  POMGR_SNP.ADT_COLORSTYLE_MERGE
INNER JOIN POMGR_SNP.USERS
ON
  POMGR_SNP.ADT_COLORSTYLE_MERGE.USER_ID = POMGR_SNP.USERS.ID
ORDER BY
  POMGR_SNP.ADT_COLORSTYLE_MERGE.DATE_OF_MERGE DESC;

spool off
exit;
