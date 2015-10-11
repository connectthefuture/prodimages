FROM sampleskuimport LEFT JOIN `data_imagepaths`.`zimages1_photoselects` ON `sampleskuimport`.`colorstyle` = `zimages1_photoselects`.`colorstyle` WHERE `zimages1_photoselects`.`colorstyle` like




SELECT `tsnp`.`colorstyle`, `tsnp`.`brand`, `tsnp`.`production_status`, `tsnp`.`gender`, `tsnp`.`category`, `tsnp`.`product_type`, `tpush`.`file_path`, `tpush`.`photo_date`
FROM `data_imagepaths`.`product_snapshot` tsnp
LEFT OUTER JOIN `data_imagepaths`.`push_photoselects` tpush 
ON `tpush`.`colorstyle` = `tsnp`.`colorstyle`
WHERE `tsnp`.`production_status` = "Production Incomplete"
ORDER BY `tsnp`.`colorstyle` DESC

sed 's/'$one'/'$two'/g'); mv "$file" "$new_file"; done; done;



--- LAVENDER REPORT--OLD not Live
SELECT COUNT( t1.`colorstyle` ) as "Outstanding",
t1.`event_id` as "Event_ID", t1.`ev_start`, t1.`product_category` as "Category",
COUNT( 
CASE WHEN t2.`sample_status` =  "Sample Sent to Bluefly" OR t2.`sample_status` =  "Scanned In at Bluefly"
THEN 1 
ELSE NULL 
END ) as "Smpl_NY",
COUNT( 
CASE WHEN t2.`sample_status` =  "Pending Sample"
THEN 1 
ELSE NULL 
END ) as "Pnd_Smpl",
COUNT( 
CASE WHEN t1.`image_dt` =  '0000-00-00'
THEN 1 
ELSE NULL 
END ) as "Need_Img",
COUNT( 
CASE WHEN t1.`copy_dt` =  '0000-00-00'
THEN 1 
ELSE NULL 
END ) as "Need_Copy",
t1.`event_title` as "Event_Title", t1.`event_group` as "Group"
FROM  `data_imports`.`events_style_statusplus` t1
left join `data_imagepaths`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle`
WHERE t1.`ev_start` 
BETWEEN SYSDATE( ) - INTERVAL 1 
DAY AND SYSDATE( ) + INTERVAL 21 
DAY
AND
t1.`production_status` = "Production Incomplete"
GROUP BY t1.`event_id` , t1.`production_status` , t1.`event_title`, t1.`product_category` , t1.`ev_start`
ORDER by t1.`event_id`

------COMPLETION REPORTS VIEWS
SELECT *
FROM viewlive_count_prodcomplete v3
left outer join viewlive_count_retouch v1 on v3.Prod_Complete = v1.Retouching_Done  
left outer join viewlive_count_copy v2 on v3.Prod_Complete = v2.Copy_Done
left outer join viewcount_photography v4 on v3.Prod_Complete = v4."Total Shots"
LIMIT 10

SELECT v1.Colorstyles, v2.Colorstyles, v3.Colorstyles
FROM viewlive_count_prodcomplete v3
join viewlive_count_retouch v1 on v3.Prod_Complete = v1.Retouching_Done  
join viewlive_count_copy v2 on v3.Prod_Complete = v2.Copy_Done  
LIMIT 5

SELECT *
FROM viewlive_count_prodcomplete v3
left outer join viewlive_count_retouch v1 on v3.Prod_Complete = v1.Retouching_Done  
left outer join viewlive_count_copy v2 on v3.Prod_Complete = v2.Copy_Done
left outer join viewcount_photography v4 on v3.Prod_Complete = v4.Shoot_Date
LIMIT 10



SELECT COUNT( t1.`colorstyle` ) as "Outstanding",
t1.`product_category` as "Category",
COUNT( 
CASE WHEN t1.`sample_status` =  "Scanned In at Bluefly" AND t1.`status_dt` = SYSDATE()
THEN 1 
ELSE NULL 
END ) as "Arrived_Today",
COUNT( 
CASE WHEN t1.`sample_status` =  "Scanned Out to Warehouse" AND t1.`status_dt` = SYSDATE()
THEN 1 
ELSE NULL 
END ) as "Returned_Today",
COUNT( 
CASE WHEN t1.`image_dt` =  SYSDATE( )
THEN 1 
ELSE NULL 
END ) as "Img_Done",
COUNT( 
CASE WHEN t1.`copy_dt` =  SYSDATE( )
THEN 1 
ELSE NULL 
END ) as "Copy_Done",
COUNT( 
CASE WHEN t1.`production_complete_dt` =  SYSDATE( )
THEN 1 
ELSE NULL 
END ) as "Prd_Complete",
FROM
     `data_imports`.`product_snapshot_live` t1

WHERE
     product_snapshot_live.sample_status = "Scanned In at Bluefly"
     OR product_snapshot_live.sample_status = "Scanned Out to Warehouse" 
GROUP BY t1.`production_status`, t1.`product_category`
