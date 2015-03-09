---UPS Tracking View

CREATE
  VIEW POMGR_SNP.V_PRODUCT_COLOR_SAMPLE_DETAIL AS
SELECT
  product_color.id product_color_id,
  sku.sku_code,
  sample.id sample_id,
  sample_tracking.create_dt sample_tracking_create_dt,
  sample_status.name sample_status_name,
  sample_box.tracking_number bluefly_tracking_number,
  filltek_tracking_number.ref_number filltek_sample_tracking_number
FROM
  pomgr_snp.product_color product_color
JOIN pomgr_snp.sample sample
ON
  sample.product_color_id = product_color.id
JOIN pomgr_snp.sku sku
ON
  sample.sku_id = sku.id
JOIN pomgr_snp.sample_tracking sample_tracking
ON
  sample_tracking.sample_id = sample.id
JOIN pomgr_snp.lk_sample_status sample_status
ON
  sample_status.id = sample_tracking.status_id
LEFT OUTER JOIN pomgr_snp.sample_box_item box_item
ON
  box_item.sample_id = sample.id
LEFT OUTER JOIN pomgr_snp.sample_box sample_box
ON
  sample_box.id = box_item.sample_box_id
LEFT OUTER JOIN pomgr_snp.sample_tracking_number filltek_tracking
ON
  filltek_tracking.sample_id = sample.id
LEFT OUTER JOIN pomgr_snp.tracking_number filltek_tracking_number
ON
  filltek_tracking_number.id = filltek_tracking.tracking_number_id,
  (
    SELECT
      t.sample_id,
      MAX(t.create_dt) create_dt
    FROM
      pomgr_snp.sample_tracking t
    GROUP BY
      sample_id
  )
  latest_sample_tracking
WHERE
  sample_tracking.create_dt          = latest_sample_tracking.create_dt
AND latest_sample_tracking.sample_id = sample.id
