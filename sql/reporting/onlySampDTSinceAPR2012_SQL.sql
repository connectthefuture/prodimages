SELECT DISTINCT
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  ATG_SNP.EVENT_GROUP.NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS,
  ATG_SNP.EVENT_GROUP.ID,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME
FROM
  POMGR_SNP.PRODUCT_SNAPSHOT
LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR Event_ID_StyleNumber
ON
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = Event_ID_StyleNumber.PRODUCT_COLOR_ID
LEFT JOIN ATG_SNP.EVENT_GROUP
ON
  ATG_SNP.EVENT_GROUP.ID = Event_ID_StyleNumber.EVENT_ID
WHERE
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= to_date('01-JAN-2012','dd-MM-yyyy')
GROUP BY
  POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE,
  POMGR_SNP.PRODUCT_SNAPSHOT.BRAND,
  ATG_SNP.EVENT_GROUP.NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.COPY_READY,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.PRODUCTION_STATUS,
  ATG_SNP.EVENT_GROUP.ID,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS,
  POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME,
  POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME
ORDER BY
   POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC,
   MAX(DISTINCT ATG_SNP.EVENT_GROUP.ID);