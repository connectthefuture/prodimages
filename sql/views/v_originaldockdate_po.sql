--Dock date view by po
CREATE
  VIEW POMGR_SNP.V_DOCK_DATES AS
SELECT
  po_hdr_id,
  shipment_number,
  MIN(dock_date) AS original_dock_date
FROM
  pomgr.adt_shp_hdr@BFYPRD1
WHERE
  dock_date IS NOT NULL
GROUP BY
  po_hdr_id,
  shipment_number
ORDER BY
  po_hdr_id,
  shipment_number
