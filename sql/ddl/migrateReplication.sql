-- ----------------------------------------------------------------------------
-- MySQL Workbench Migration
-- Migrated Schemata: data_imports, images_photoselects_jpg, images_retouched_jpg, upload_alt_jpg-png, upload_primary_jpg-png
-- Source Schemata: data_imports, images_photoselects_jpg, images_retouched_jpg, upload_alt_jpg-png, upload_primary_jpg-png
-- Created: Mon Sep 17 13:19:05 2012
-- ----------------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;;

-- ----------------------------------------------------------------------------
-- Schema data_imports
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `data_imports` ;
CREATE SCHEMA IF NOT EXISTS `data_imports` ;

-- ----------------------------------------------------------------------------
-- Table data_imports.file7_sumlist
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `data_imports`.`file7_sumlist` (
  `sql_id` BIGINT(20) NOT NULL AUTO_INCREMENT ,
  `COLORSTYLE` INT(9) NOT NULL ,
  `PHOTO_DATE` DATE NOT NULL ,
  `FILE_PATH` VARCHAR(250) CHARACTER SET 'utf8' NOT NULL ,
  PRIMARY KEY (`sql_id`) ,
  UNIQUE INDEX `FILE_PATH` (`FILE_PATH` ASC) ,
  INDEX `COLORSTYLE` (`COLORSTYLE` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin
COMMENT = 'File7 Daily Summary of all Files aka stylestringtest';

-- ----------------------------------------------------------------------------
-- Table data_imports.product_snapshot
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `data_imports`.`product_snapshot` (
  `MASTER_STYLE` BIGINT(20) NOT NULL ,
  `COLORSTYLE` BIGINT(38) NOT NULL ,
  `SKU` VARCHAR(20) NULL DEFAULT NULL ,
  `PO_HDR` BIGINT(38) NULL DEFAULT NULL ,
  `ACTIVE` CHAR(1) NULL DEFAULT NULL ,
  `MAIN_IMAGE` CHAR(1) NULL DEFAULT NULL ,
  `ZOOM_IMAGE` CHAR(1) NULL DEFAULT NULL ,
  `ALT_1` CHAR(1) NULL DEFAULT NULL ,
  `ALT_2` CHAR(1) NULL DEFAULT NULL ,
  `ALT_3` CHAR(1) NULL DEFAULT NULL ,
  `ALT_4` CHAR(1) NULL DEFAULT NULL ,
  `ALT_5` CHAR(1) NULL DEFAULT NULL ,
  `IMAGE_SWATCH` VARCHAR(1000) NULL DEFAULT NULL ,
  `COPY_READY` DATE NULL DEFAULT NULL ,
  `IMAGE_READY` DATE NULL DEFAULT NULL ,
  `PRODUCTION_STATUS` VARCHAR(255) NULL DEFAULT NULL ,
  `PRODUCTION_COMPLETE_DT` DATE NULL DEFAULT NULL ,
  `MERCHANT_STATUS` VARCHAR(255) NULL DEFAULT NULL ,
  `MERCHANT_COMPLETE_DT` DATE NULL DEFAULT NULL ,
  `START_DATE` DATE NULL DEFAULT NULL ,
  `END_DATE` DATE NULL DEFAULT NULL ,
  `ORIGINAL_START_DATE` DATE NULL DEFAULT NULL ,
  `INACTIVE_DEPARTMENT` BIGINT(38) NULL DEFAULT NULL ,
  `INACTIVE_REASON` VARCHAR(1000) NULL DEFAULT NULL ,
  `DNA_FLAG` CHAR(1) NULL DEFAULT NULL ,
  `SEASON` VARCHAR(255) NULL DEFAULT NULL ,
  `YEAR` BIGINT(4) NULL DEFAULT NULL ,
  `ORIGINAL_SEASON` VARCHAR(255) NULL DEFAULT NULL ,
  `ORIGINAL_YEAR` BIGINT(4) NULL DEFAULT NULL ,
  `BRAND` VARCHAR(255) NULL DEFAULT NULL ,
  `BRAND_TYPE` VARCHAR(255) NULL DEFAULT NULL ,
  `VENDOR_SIZE_CHART` VARCHAR(255) NULL DEFAULT NULL ,
  `BLUEFLY_SIZE_CHART` VARCHAR(255) NULL DEFAULT NULL ,
  `VENDOR_SIZE_VALUE` VARCHAR(255) NULL DEFAULT NULL ,
  `BLUEFLY_SIZE_VALUE` VARCHAR(255) NULL DEFAULT NULL ,
  `COUNTRY_OF_ORIGIN` VARCHAR(2) NULL DEFAULT NULL ,
  `FUR_ORIGIN` VARCHAR(255) NULL DEFAULT NULL ,
  `MATERIAL` VARCHAR(300) NULL DEFAULT NULL ,
  `CARE_INSTRUCTIONS` VARCHAR(40) NULL DEFAULT NULL ,
  `PRODUCT_SPECIAL_INFO` VARCHAR(255) NULL DEFAULT NULL ,
  `PRODUCT_SIZE_CHART` VARCHAR(255) NULL DEFAULT NULL ,
  `GIFT_WRAP` CHAR(1) NULL DEFAULT NULL ,
  `PRODUCT_SHORT_NAME` VARCHAR(255) NULL DEFAULT NULL ,
  `PRODUCT_LONG_DESCRIPTION` VARCHAR(1000) NULL DEFAULT NULL ,
  `COLOR_GROUP` VARCHAR(255) NULL DEFAULT NULL ,
  `COLOR_DESCRIPTION` VARCHAR(255) NULL DEFAULT NULL ,
  `VENDOR_STYLE_NO` VARCHAR(255) NULL DEFAULT NULL ,
  `BULLET_1` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_2` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_3` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_4` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_5` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_6` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_7` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_8` VARCHAR(1024) NULL DEFAULT NULL ,
  `BULLET_9` VARCHAR(1024) NULL DEFAULT NULL ,
  `WEIGHT` BIGINT(38) NULL DEFAULT NULL ,
  `PERFECT_MATCH` BIGINT(38) NULL DEFAULT NULL ,
  `KEYWORD_DESIGN` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_MATERIAL` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_STYLE_1` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_STYLE_2` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_STYLE_3` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_FIT` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_OCCASION` VARCHAR(50) NULL DEFAULT NULL ,
  `KEYWORD_TREND` VARCHAR(50) NULL DEFAULT NULL ,
  `CORETMETRICS_CATEGORY` VARCHAR(32) NULL DEFAULT NULL ,
  `BML_CODE` VARCHAR(42) NULL DEFAULT NULL ,
  `TAX_CODE` VARCHAR(85) NULL DEFAULT NULL ,
  `FIRST_COST` BIGINT(38) NULL DEFAULT NULL ,
  `WHOLESALE` BIGINT(38) NULL DEFAULT NULL ,
  `MSRP` BIGINT(38) NULL DEFAULT NULL ,
  `BLUEFLY` BIGINT(38) NULL DEFAULT NULL ,
  `PRICE` BIGINT(38) NULL DEFAULT NULL ,
  `REDUCED_PRICE` BIGINT(38) NULL DEFAULT NULL ,
  `CLEARENCE_PRICE` BIGINT(38) NULL DEFAULT NULL ,
  `SALE_PRICE` BIGINT(38) NULL DEFAULT NULL ,
  `SELLING_PRICE` BIGINT(20) NULL DEFAULT NULL ,
  `TOTAL_RECVD` BIGINT(20) NULL DEFAULT NULL ,
  `TOTAL_ON_HAND` BIGINT(20) NULL DEFAULT NULL ,
  `AVAILABLE_ON_HAND` BIGINT(20) NULL DEFAULT NULL ,
  `LEVEL1_NAME` VARCHAR(100) NULL DEFAULT NULL ,
  `LEVEL2_NAME` VARCHAR(150) NULL DEFAULT NULL ,
  `LEVEL3_NAME` VARCHAR(200) NULL DEFAULT NULL ,
  `LEVEL4_NAME` VARCHAR(300) NULL DEFAULT NULL ,
  `LEVEL5_NAME` VARCHAR(400) NULL DEFAULT NULL ,
  `LEVEL6_NAME` VARCHAR(200) NULL DEFAULT NULL ,
  `LEVEL7_NAME` VARCHAR(100) NULL DEFAULT NULL ,
  `SAMPLE_STATUS` VARCHAR(35) NULL DEFAULT NULL ,
  `SAMPLE_STATUS_DATE` DATE NULL DEFAULT NULL ,
  `RETURN_POLICY` VARCHAR(85) NULL DEFAULT NULL ,
  `SAMPLE_IMAGE` CHAR(1) NULL DEFAULT NULL ,
  `PHOTOGRAPHED_DATE` DATE NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- ----------------------------------------------------------------------------
-- Schema images_photoselects_jpg
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `images_photoselects_jpg` ;
CREATE SCHEMA IF NOT EXISTS `images_photoselects_jpg` ;

-- ----------------------------------------------------------------------------
-- Table images_photoselects_jpg.images
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `images_photoselects_jpg`.`images` (
  `image_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `filename` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `mime_type` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `file_size` INT(11) NOT NULL ,
  `file_data` LONGBLOB NOT NULL ,
  PRIMARY KEY (`image_id`) ,
  INDEX `filename` (`filename` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Schema images_retouched_jpg
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `images_retouched_jpg` ;
CREATE SCHEMA IF NOT EXISTS `images_retouched_jpg` ;

-- ----------------------------------------------------------------------------
-- Table images_retouched_jpg.images
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `images_retouched_jpg`.`images` (
  `image_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `filename` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `mime_type` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `file_size` INT(11) NOT NULL ,
  `file_data` LONGBLOB NOT NULL ,
  PRIMARY KEY (`image_id`) ,
  INDEX `filename` (`filename` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Schema upload_alt_jpg-png
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `upload_alt_jpg-png` ;
CREATE SCHEMA IF NOT EXISTS `upload_alt_jpg-png` ;

-- ----------------------------------------------------------------------------
-- Table upload_alt_jpg-png.images
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `upload_alt_jpg-png`.`images` (
  `image_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `filename` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `mime_type` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `file_size` INT(11) NOT NULL ,
  `file_data` LONGBLOB NOT NULL ,
  PRIMARY KEY (`image_id`) ,
  INDEX `filename` (`filename` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- ----------------------------------------------------------------------------
-- Schema upload_primary_jpg-png
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `upload_primary_jpg-png` ;
CREATE SCHEMA IF NOT EXISTS `upload_primary_jpg-png` ;

-- ----------------------------------------------------------------------------
-- Table upload_primary_jpg-png.images
-- ----------------------------------------------------------------------------
CREATE  TABLE IF NOT EXISTS `upload_primary_jpg-png`.`images` (
  `image_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `filename` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `mime_type` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL ,
  `file_size` INT(11) NOT NULL ,
  `file_data` LONGBLOB NOT NULL ,
  PRIMARY KEY (`image_id`) ,
  INDEX `filename` (`filename` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;
SET FOREIGN_KEY_CHECKS = 1;;
