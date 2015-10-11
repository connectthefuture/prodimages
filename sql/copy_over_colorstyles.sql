set echo off
set verify off
set termout on
set array 3000                      
-- set heading on
-- set headsep on
set pagesize 50000
set colsep "~"
set pages 50000
set feedback off
--set tab on
--set trimspool on 
set trimout on
set null "NULL"
set newpage none
set linesize 25000

SELECT DISTINCT
  pomgr_snp.product_snapshot.COLORSTYLE AS "PRODUCT_COLOR_ID",
  pomgr_snp.product_snapshot.MATERIAL,
  pomgr_snp.product_snapshot.PRODUCT_SHORT_NAME       AS "SHORT_NAME",
  POMGR_SNP.COLOR_GROUP.ID as "COLOR_GROUP_ID",
  pomgr_snp.product_snapshot.BULLET_1,
  pomgr_snp.product_snapshot.BULLET_2,
  pomgr_snp.product_snapshot.BULLET_3,
  pomgr_snp.product_snapshot.BULLET_4,
  pomgr_snp.product_snapshot.BULLET_5,
  pomgr_snp.product_snapshot.BULLET_6,
  pomgr_snp.product_snapshot.BULLET_7,
  -- pomgr_snp.product_snapshot.BULLET_8,
  -- pomgr_snp.product_snapshot.BULLET_9,
  pomgr_snp.product_snapshot.PRODUCT_LONG_DESCRIPTION AS "LONG_DESCRIPTION",
  pomgr_snp.product_snapshot.COUNTRY_OF_ORIGIN        AS "COUNTRY_ORIGIN",
  pomgr_snp.product_snapshot.COPY_READY        AS "COPY_READY_DT"
FROM
  pomgr_snp.product_snapshot
INNER JOIN POMGR_SNP.COLOR_GROUP
ON
  pomgr_snp.product_snapshot.COLOR_GROUP = POMGR_SNP.COLOR_GROUP.DESCRIPTION
WHERE
  pomgr_snp.product_snapshot.COLORSTYLE IN ('&1');
exit;
﻿﻿
