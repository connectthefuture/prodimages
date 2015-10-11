<?php
//$db_local_hostname = "prodimages.ny.bluefly.com:3301";
$db_local_hostname = "127.0.0.1:3301";
$db_local_database = 'data_imagepaths';
//$db_local_database = 'data_imports';
$db_local_username = 'root';
$db_local_password = 'mysql';


//Connect to MySQL Server
$db_local_server = mysql_connect($db_local_hostname, $db_local_username, $db_local_password);
if (!$db_local_server)
	die("Unable to connect to MySQL: " . mysql_error());
//echo "$db_local_server";
//print $_POST['attval_1'];
//Select Database
mysql_select_db($db_local_database) or die("Unable to select database: " . mysql_error());

//Get POST Data for Date Params for Query - uses JavaScript

function GetDateSelectString($IsPosted = true, $photodate = '') {
	if ($IsPosted) {
		return (int) $_POST[$photodate . 'dateYR']
			. '-' . (int) $_POST[$photodate . 'datemo']
			. '-' . (int) $_POST[$photodate . 'datedy'];
	}

	return (int) $_GET[$photodate . 'dateYR']
		. '-' . (int) $_GET[$photodate . 'datemo']
		. '-' . (int) $_GET[$photodate . 'datedy'];
}

$photodate = GetDateSelectString();



//	Get POST Data for Table and Query Type Selection Variable Instansiation
//		if (isset($_POST['qtype'])) $qtype = $_POST['qtype'];
//		if (isset($_POST['qtable'])) $qtable = $_POST['qtable'];
if (isset($_POST['jointable']))
	$jointable = $_POST['jointable'];
else {
	$jointable = 'data_imagepaths.product_snapshot_live';
}
//	Get POST Data for Selected Search Fields and their Values to Search
//		if (isset($_POST['attfield_1'])) {
//			$attfield_1 = $_POST['attfield_1'];
//			$attval_1 	= $_POST['attval_1'];
//		}
//		function getValue($key) {
//    		if (!isset($_POST[$key])) {
//        		return false;
//    			}
//    		return $_POST[$key];
//			}
//
//			if (getValue('attfield_1') == 'current_style') {
//   		 // Do Something
//			 $qtable = 'data_imports.merged_styles';
//			}
// Another if process
if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'current_style') {
	// Do Something
	$qtable = "data_imports.merged_styles";
	$current_style = $_POST['attval_1'];
	$jointable_hrez = 'data_imagepaths.post_ready_original';
	$jointable_z = 'data_imagepaths.zimages1_photoselects';
	//$mergequery = "SELECT $qtable.'current_style', $qtable.'voided_style', $qtable.'vendor_style', file_path FROM $qtable LEFT JOIN 'data_imagepaths'.'zimages1_photoselects' ON $qtable.'current_style' = $jointable.'colorstyle'  WHERE $qtable.'current_style' like '%$current_style%'";


	$mergequery = "SELECT current_style, voided_style, merge_date, file_path, photo_date 
					FROM $qtable 
					LEFT JOIN $jointable_z ON $qtable.current_style = $jointable_z.colorstyle 
					WHERE $qtable.current_style like '$current_style%'
					ORDER by current_style DESC";
	// OR merged_styles.voided_style like '$current_style%'
	$query = $mergequery;
//			echo $query;
	$result = mysql_query($query);
}


//only top query works NEED TO REMOVE TRAILING WHITE SPACE FROM VOIDED COLUMN
else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'voided_style') {
	$qtable = 'data_imports.merged_styles';
	$voided_style = $_POST['attval_1'];
	$jointable_hrez = 'data_imagepaths.post_ready_original';
	$jointable_z = 'data_imagepaths.zimages1_photoselects';
	$mergequery = "SELECT current_style, voided_style, merge_date, file_path, photo_date 
					FROM $qtable 
					LEFT JOIN $jointable_z ON $qtable.voided_style = $jointable_z.colorstyle 
					WHERE $qtable.voided_style like '$voided_style%'
					ORDER by voided_style DESC";

	$query = $mergequery;
	//echo $voided_style;
	$result = mysql_query($query);
}


/// Actually the Vendor Search Works now Too Yipee!!!!
else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'vendor_style') {
	$qtable = 'data_imports.merged_styles';
	$vendor_style = $_POST['attval_1'];
	$jointable_z = 'data_imagepaths.zimages1_photoselects';
	$jointable_hrez = 'data_imagepaths.post_ready_original';
	$jointable_sampvend = 'data_imports.sampleid_vendorstyle';
	$mergequery = "SELECT current_style, voided_style, merge_date, file_path, photo_date, $jointable_sampvend.vendor_style
					FROM $qtable 
					JOIN $jointable_z 			ON $qtable.current_style = $jointable_z.colorstyle
					LEFT JOIN $jointable_sampvend 	ON $qtable.current_style = $jointable_sampvend.colorstyle
					WHERE $jointable_sampvend.vendor_style like '%$vendor_style%'
					ORDER by photo_date DESC";

	$query = $mergequery;
//			echo $query;
	$result = mysql_query($query);
}

///////////////// 	//////////////////////////////////////////////////////////////////////
else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'sample_status') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$sample_status = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];

	$samplequery = "SELECT '$qtable'.`colorstyle`, '$qtable'.`sample_status`, '$qtable'.`sample_location`, '$qtable'.`vendor_style`, file_path 
			FROM '$qtable' 
			LEFT JOIN '$jointable' ON '$qtable'.`colorstyle` = '$jointable'.`colorstyle` 
			WHERE  '$qtable'.`sample_status` like '%$sample_status%'";

	$query = $samplequery;
	$result = mysql_query($query);
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'status_dt') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$status_dt = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'sample_location') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$sample_location = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];

	$samplequery = "SELECT '$qtable'.`colorstyle`, '$qtable'.`sample_status`, '$qtable'.`sample_location`, '$qtable'.`vendor_style`, file_path 
			FROM '$qtable' 
			LEFT JOIN '$jointable' ON '$qtable'.`colorstyle` = '$jointable'.`colorstyle` 
			WHERE  '$qtable'.`sample_status` like '%$sample_location%'";

	$query = $samplequery;
	$result = mysql_query($query);
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'sample_id') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$sample_id = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'sample_dt') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$sample_dt = $_POST['sample_dt'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'UPS_TrackingID') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$UPS_TrackingID = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'Tracking_Date') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$Tracking_Date = $_POST['Tracking_Date'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'SampleID') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	$SampleID = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'IPTC:SampleInventory') {
	$qtable = 'data_imports.sampleid_vendorstyle';
	//"$IPTC:SampleInventory" = $_POST['attval_1'];
	$vendor_style = $_POST['vendor_style'];
}



////////////////// Regular Search	/////////////////	
else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'colorstyle') {
	$qtable = 'data_imagepaths.zimages1_photoselects';
	$jointable_prdsnp = 'data_imagepaths.product_snapshot_live';
	$jointable_hrez = 'data_imagepaths.post_ready_original';
	$colorstyle = $_POST['attval_1'];
//				if(isset($_POST['searchtype']) && $_POST['searchtype'] == 'checkhirez')
//				{
//				echo "Uncheck the Checkboxes. They don't work yet.";
//				}
	//////		
	/// DATE SEARCH if Check Box SET
	if (isset($_POST['checkdate']) && $_POST['datemo'] !== '0') {
		//echo $photodate;
		//echo "THIS DATE SEARCH DOES NOT WORK. JUST GO BACK AND DO IT RIGHT";

		$stylequery = "SELECT tzimg.colorstyle, tpsnp.brand, tpsnp.production_status, tzimg.file_path, tzimg.photo_date, threz.file_path, tzimg.alt
					FROM $qtable tzimg
					JOIN $jointable_prdsnp tpsnp ON tzimg.colorstyle = tpsnp.colorstyle					
					JOIN data_imagepaths.post_ready_original threz ON ( tzimg.colorstyle = threz.colorstyle AND tzimg.alt = threz.alt )
					WHERE tzimg.photo_date = '$photodate'
					ORDER by tzimg.photo_date DESC, tzimg.colorstyle, tzimg.alt";
	}
	////////////////// DATE SEARCH DONT WORK YET SO ELSE IT IS		
	else {
	/////// ELSE ITS A REGULAR SEARCH BY STYLE NUMBER
		$stylequery = "SELECT tzimg.colorstyle, tpsnp.brand, tpsnp.production_status, tzimg.file_path, tzimg.photo_date, threz.file_path, tzimg.alt
					FROM $qtable tzimg
					JOIN $jointable_prdsnp tpsnp ON tzimg.colorstyle = tpsnp.colorstyle					
					JOIN data_imagepaths.post_ready_original threz ON ( tzimg.colorstyle = threz.colorstyle AND tzimg.alt = threz.alt )
					WHERE tzimg.colorstyle like '$colorstyle%'
					ORDER by tzimg.photo_date DESC, tzimg.colorstyle, tzimg.alt";
	}

	$query = $stylequery;
	$result = mysql_query($query);
}

//////////////////////////////////////////////////////////////////////////////			
else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'brand') {
	$qtable = 'data_imagepaths.zimages1_photoselects';
	$jointable = 'data_imagepaths.product_snapshot_live';
	$brand = $_POST['attval_1'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'gender') {
	$qtable = 'data_imagepaths.zimages1_photoselects';
	$jointable = 'data_imagepaths.product_snapshot_live';
	$gender = $_POST['attval_1'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'category') {
	$qtable = 'data_imagepaths.zimages1_photoselects';
	$jointable = 'data_imagepaths.product_snapshot_live';
	$category = $_POST['attval_1'];
} else if (isset($_POST['attfield_1']) && $_POST['attfield_1'] == 'product_type') {
	$qtable = 'data_imagepaths.zimages1_photoselects';
	$jointable = 'data_imagepaths.product_snapshot_live';
	$product_type = $_POST['attval_1'];
}

//echo $qtable;
//echo $attfield_1;
//echo $attval_1;
//echo $query;
//		echo $result;




if (isset($query)) {
	$result = mysql_query($query);
}


if (!$result)
	die("Database access failed: " . mysql_error());


$rows = mysql_num_rows($result);

if ($rows != '0') {

	echo '<a name="totals"><span>Total Images Found: <b><u>' . $rows . '</u></b><href=</a></span>';

////		///////
	///////////////
////////////////////// TWO OUTPUT OPTIONS IF its merge info do the first chunk, for HiRez its the second chunk	////////////////        
	if (isset($mergequery)) {

		print '<html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <script type="text/javascript" src="common.js"></script>
        <script type="text/javascript" src="jquery.js"></script>
		<link href="site_stylesheet.css" rel="stylesheet" type="text/css" />
        <title>Merge Query</title>';


		print '</head>';

		while ($row = mysql_fetch_array($result)) {

			print '<body>';

			print '<table border="1" width="auto" cols="2">
        
               
				 	<div class="desc"><b>' . $row[0] . '</b></div>
					
					 <tr>
                          <th align="left" scope="row">Current Style</th>
                          <td>' . $row[0] . '</td>
                        </tr>
                        <tr>
                          <th align="left" scope="row">Voided Style</th>
                          <td>' . $row[1] . '</td>
                        </tr>
                        <tr>
                          <th align="left" scope="row">Merge Date</th>
                          <td>' . $row[2] . '</td>
                        </tr>
						<tr>
                          <th align="left" scope="row">Photo Date</th>
                          <td>' . $row[4] . '</td>
                        </tr>
						<tr>
                          <th align="left" scope="row">Vendor Style</th>
                          <td>' . $row[5] . '</td>
                        </tr>
					<tr>
					  <a href="' . $row[3] . '"><img src="' . $row[3] . '" width="100" height="120" alt="' . $row[0] . '" /></a>
					  
					</tr>
					
        
        </table>
		<hr align="left" width="25%" size="2" color="#336699" />';



			print '</body>';
		}

		print '</html>';
	}



////////////////////		///	//////	//////////////////////////	///////////	///////
	////////////////////// If YOU WANT HIGH REZ YOU WANT THE FOLLOWING ///////////////////////////////
////////////////////////////////	////////////	//////////	/////////////////////////////////////			
	elseif (isset($stylequery)) {

		print '<html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <script type="text/javascript" src="common.js"></script>
        <script type="text/javascript" src="jquery.js"></script>
		<link href="site_stylesheet.css" rel="stylesheet" type="text/css" />
        <title>Search Results</title>';


		print '</head>';

		while ($row = mysql_fetch_array($result)) {

			print '<body>';

			print '<table border="1" width="auto" cols="2">
        
               
				 	<div class="desc"><b>' . $row[0] . '</b></div>
					
					 <tr>
                          <th align="left" scope="row">Style Number</th>
                          <td>' . $row[0] . '</td>
                        </tr>
                        <tr>
                          <th align="left" scope="row">Brand</th>
                          <td>' . $row[1] . '</td>
                        </tr>
                        <tr>
                          <th align="left" scope="row">Status</th>
                          <td>' . $row[2] . '</td>
                        </tr>
						<tr>
                          <th align="left" scope="row">Photo Date</th>
                          <td>' . $row[4] . '</td>
                        </tr>
						<tr>
                          <th align="left" scope="row">Alt Img Number</th>
                          <td>' . $row[6] . '</td>
                        </tr>
					<tr>
					  <a href="' . $row[5] . '"><img src="' . $row[3] . '" width="100" height="120" alt="' . $row[0] . '" /></a>
					  
					</tr>
					
        
        </table>
		<hr align="left" width="25%" size="2" color="#336699" />';



			print '</body>';
		}

		print '</html>';
	}
} else {
	print '<html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <script type="text/javascript" src="common.js"></script>
        <script type="text/javascript" src="jquery.js"></script>
		<link href="site_stylesheet.css" rel="stylesheet" type="text/css" />
        <title>Absolute Failure</title>';


	print '</head>';

	print '<body><a href="genericQuery_client.html"><img src="noresults.png" height="800" width="800" alt="Go Back And Try Again" onclick="genericQuery_client.html"/></a>';

	print '</body>';


	print '</html>';
}
?>
