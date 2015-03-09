set echo off
set verify off
set termout on
set array 3000                      
--set heading on
--set headsep ","
set pagesize 50000
set colsep ","
set pages 50000
set feedback off
--set tab on
set trimspool off
--set recsep "|"
--set trimout on
set null "-"
set newpage none
set linesize 5000
spool /mnt/Post_Ready/zProd_Server/imageServer7/tmp/limbo/spoolDWsample_whseSkuimport.csv

SELECT
  POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID                                AS "colorstyle",
  POMGR_SNP.PO_LINE.PO_HDR_ID                                       AS "po_number",
  POMGR_SNP.INVENTORY.SKU_CODE                                      AS "sku",
  POMGR_SNP.SHP_HDR.RECEIVING_STATUS                                AS "receiving_status",
  to_date(POMGR_SNP.SHP_HDR.DOCK_DATE, 'YYYY-MM-DD')                AS "dock_date",
  to_date(POMGR_SNP.SHP_HDR.IN_RECEIVING_DATE, 'YYYY-MM-DD')        AS "in_receiving_date",
  to_date(POMGR_SNP.SHP_HDR.RECEIVE_DATE, 'YYYY-MM-DD')             AS "receive_date",
  POMGR_SNP.PO_SKU.ORDERED_COUNT                                    AS "quantity_ordered",
  POMGR_SNP.INVENTORY.TOTAL_WH_RCVD_QTY                             AS "quantity_received",
  POMGR_SNP.INVENTORY.AVAL_ON_HAND                                  AS "quantity_onhand",
  to_date(POMGR_SNP.PO_SKU.WH_TRANSMITTED_DATE, 'YYYY-MM-DD')       AS "wh_transmit_date",
  to_date(POMGR_SNP.SHP_HDR.SENT_TO_WAREHOUSE_DATE, 'YYYY-MM-DD')   AS "vendor_ship_date",
  to_date(POMGR_SNP.SHP_HDR.IN_TRANSIT_DATE, 'YYYY-MM-DD')          AS "vendor_intransit_date",
  to_date(POMGR_SNP.SHP_HDR.EXPECTED_DATE, 'YYYY-MM-DD')            AS "wh_expected_date",
  POMGR_SNP.SHP_HDR.SHIPMENT_NUMBER                                 AS "shipment_number",
  POMGR_SNP.SHP_HDR.CARTON_COUNT                                    AS "shipment_carton_count",
  to_date(POMGR_SNP.SHP_HDR.CREATED_DATE, 'YYYY-MM-DD')             AS "shipment_create_date",
  POMGR_SNP."SAMPLE".STATUS_ID                                      AS "StatusSample_ID",
  POMGR_SNP.TRACKING_NUMBER.REF_NUMBER                              AS "UPS_TrackingID",
  to_date(POMGR_SNP.TRACKING_NUMBER.CREATE_DT, 'YYYY-MM-DD')        AS "Tracking_Date",
  POMGR_SNP.SHP_HDR.RECEIVING_STATUS_ID                             AS "receiving_status_id",
  POMGR_SNP.SAMPLE_TRACKING_NUMBER.SAMPLE_ID                        AS "sample_id",
  POMGR_SNP.VENDOR_SIZE_VALUE.NAME                                  AS "vendor_size",
  POMGR_SNP.VENDOR_SIZE_VALUE.BFLY_SIZE_VALUE_ID                    AS "bluefly_size",
  POMGR_SNP.VENDOR_SIZE_VALUE.SAMPLE_SIZE                           AS "sample_flag",
  POMGR_SNP.SHP_SKU.SHP_HDR_ID                                      AS "shipment_hdr_id",
  POMGR_SNP.PO_SKU.SKU_ID                                           AS "sku_id",
  POMGR_SNP.SKU.VENDOR_SIZE_VALUE_ID                                AS "vendor_size_id",
  POMGR_SNP.PO_LINE.REPLENISH_FLAG                                  AS "replenish_flag",
  POMGR_SNP.USERS.USERNAME                                          AS "username"
FROM
  POMGR_SNP.PO_HDR
LEFT JOIN POMGR_SNP.SHP_HDR
ON
  POMGR_SNP.PO_HDR.USER_ID = POMGR_SNP.SHP_HDR.PO_HDR_ID
FULL JOIN POMGR_SNP.SHP_SKU
ON
  POMGR_SNP.SHP_HDR.ID = POMGR_SNP.SHP_SKU.SHP_HDR_ID
INNER JOIN POMGR_SNP.USERS
ON
  POMGR_SNP.USERS.ID = POMGR_SNP.PO_HDR.USER_ID
LEFT JOIN POMGR_SNP.PO_LINE
ON
  POMGR_SNP.PO_HDR.ID = POMGR_SNP.PO_LINE.PO_HDR_ID
INNER JOIN POMGR_SNP.PO_SKU
ON
  POMGR_SNP.PO_LINE.ID = POMGR_SNP.PO_SKU.PO_LINE_ID
INNER JOIN POMGR_SNP.SKU
ON
  POMGR_SNP.PO_SKU.SKU_ID = POMGR_SNP.SKU.ID
INNER JOIN POMGR_SNP.INVENTORY
ON
  POMGR_SNP.PO_SKU.PO_LINE_ID = POMGR_SNP.INVENTORY.SKU_ID
INNER JOIN POMGR_SNP.VENDOR_SIZE_VALUE
ON
  POMGR_SNP.SKU.VENDOR_SIZE_VALUE_ID = POMGR_SNP.VENDOR_SIZE_VALUE.ID
INNER JOIN POMGR_SNP."SAMPLE"
ON
  POMGR_SNP."SAMPLE".SKU_ID = POMGR_SNP.PO_SKU.SKU_ID
INNER JOIN POMGR_SNP.SAMPLE_TRACKING_NUMBER
ON
  POMGR_SNP."SAMPLE".ID = POMGR_SNP.SAMPLE_TRACKING_NUMBER.SAMPLE_ID
INNER JOIN POMGR_SNP.TRACKING_NUMBER
ON
  POMGR_SNP.SAMPLE_TRACKING_NUMBER.TRACKING_NUMBER_ID = POMGR_SNP.TRACKING_NUMBER.ID
WHERE
  POMGR_SNP.TRACKING_NUMBER.CREATE_DT >= TRUNC((SysDate) - 90)
ORDER BY
  POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last,
  to_date(POMGR_SNP.TRACKING_NUMBER.CREATE_DT, 'YYYY-MM-DD') DESC Nulls Last;
spool off
exit;
