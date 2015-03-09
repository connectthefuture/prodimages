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
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spool_upcomingpos.csv

SELECT DISTINCT
  POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID as "colorstyle",
  POMGR_SNP.V_PO.PO as "po_num",
  to_date( POMGR_SNP.V_PO.START_DATE, 'YYYY-MM-DD') as "postrt_dt",
  to_date( POMGR_SNP.V_PO.END_DATE, 'YYYY-MM-DD') as "poend_dt",
  POMGR_SNP.V_PO.NO_OF_SHIPMENTS as "shipment_ct",
  to_date(POMGR_SNP.V_PO.SENT_TO_WAREHOUSE_DATE, 'YYYY-MM-DD') as "sentwh_dt",
  to_date(POMGR_SNP.V_PO.DOCK_DATE, 'YYYY-MM-DD') as "dock_dt",
  to_date(POMGR_SNP.V_PO.IN_RECEIVING_DATE, 'YYYY-MM-DD') as "inrec_dt",
  to_date(POMGR_SNP.V_PO.RECEIVE_DATE, 'YYYY-MM-DD') as "recvd_dt",
  POMGR_SNP.V_PO.PO_STYLES as "po_total_styles",
  POMGR_SNP.V_PO.PO_STATUS as "po_status",
  to_date(POMGR_SNP.V_PO.SAMPLE_DATE, 'YYYY-MM-DD') as "sample_dt",
  POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE as "vendor_style",
  to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') as "copy_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR.IMAGE_READY_DT, 'YYYY-MM-DD') as "image_dt",
  to_date(POMGR_SNP.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD') as "prdcmp_dt",
  POMGR_SNP.LK_PRODUCT_STATUS.NAME as "production_status",
  POMGR_SNP.LK_SAMPLE_STATUS.NAME as "sample_status",
  POMGR_SNP.LK_SAMPLE_LOCATION.NAME AS "sample_location"
FROM
  POMGR_SNP.V_PO
RIGHT JOIN POMGR_SNP.PO_LINE
ON
  POMGR_SNP.PO_LINE.PO_HDR_ID = POMGR_SNP.V_PO.PO
LEFT JOIN POMGR_SNP.PRODUCT_COLOR
ON
  POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID = POMGR_SNP.PRODUCT_COLOR.ID
LEFT JOIN POMGR_SNP."SAMPLE"
ON
  POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID = POMGR_SNP."SAMPLE".PRODUCT_COLOR_ID
LEFT JOIN POMGR_SNP.LK_SAMPLE_STATUS
ON
  POMGR_SNP."SAMPLE".STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID
LEFT JOIN POMGR_SNP.LK_SAMPLE_LOCATION
ON
  POMGR_SNP.LK_SAMPLE_LOCATION.ID = POMGR_SNP.LK_SAMPLE_STATUS.LOCATION_ID
LEFT JOIN POMGR_SNP.LK_PRODUCT_STATUS
ON
  POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
WHERE
  POMGR_SNP.V_PO.PO_STATUS LIKE 'Approved'
AND POMGR_SNP.V_PO.START_DATE <= TRUNC(SysDate + 90)
AND POMGR_SNP.V_PO.START_DATE >= TRUNC(SysDate - 14)
ORDER BY
  to_date(POMGR_SNP.V_PO.START_DATE, 'YYYY-MM-DD') DESC Nulls Last;
  
spool off
exit;
