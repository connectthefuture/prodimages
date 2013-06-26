<?php

require_once('../../conf/globals-3301.php');

////////////////////////////////////////////////////////////
//////////////
//////
/////////////////////////////////////////////////
//////										////////////////
///////										////////////////
//////	Set Database and Tables	for Query or Script	////////
//////////////								////////////////
/////////////////////////////////////////////////
////////////////////
////////
if (isset($_POST['qbase']))
    $db_local_database = '';
    $db_local_database = $_POST['qbase'];
    $qbase = $_POST['qbase'];


if (isset($_POST['qtable']))
    $qtable = $_POST['qtable'];
else
    $qtable = 'imgsrv7_photoselects';

if (!mysql_select_db($db_local_database, $db)) {
    echo "Unable to connect to database";
    exit;
}
//echo "$db_local_database";

///////////////////////////////////////
// Sanitize User Input of _POST data
//////
// Get _POST array Data from Form input and Build Query
//////
/////////////////////////////////////////
//////	Simple Search by Style	////////
/////////////////////////////////////////
/////
//if (is_numeric($_POST['stylesearch']))
 //   $query = "SELECT * FROM $qtable WHERE colorstyle = '$style'";
//else  $query = "SELECT * FROM $qtable WHERE colorstyle = '$style'";
if (is_numeric($_POST['style']))
    $query = "SELECT * FROM $qtable WHERE filename = '$style'";
//else  $query = "SELECT * FROM $qtable WHERE filename = '$style'";

//elseif (isset($_POST['style']))
//else 
//    $query = "SELECT * FROM $qtable";
//$query_select = "SELECT * FROM $qtable ";
//
/////
//	Search using Parameters Dept, Category, Product Type, PrdStatus, SampleStatus	/////
/////
//
////
if (isset($_POST['level2_name']))
    $level2_name = $_POST['level2_name'];
else
    $level2_name = "women";

if (isset($_POST['level3_name']))
    $level3_name = $_POST['level3_name'];
else
    $level3_name = "apparel";
    
if (isset($_POST['level4_name']))
    $level4_name = $_POST['level4_name'];
else
    $level4_name = "dresses";

if (isset($_POST['sample_status']))
    $sample_status = $_POST['sample_status'];
else
    $sample_status = "scanned_in_at_bluefly";

if (isset($_POST['production_status']))
    $production_status = $_POST['production_status'];

/////	///////	 $query = "SELECT * FROM '$qtable' WHERE LEVEL2_NAME='$level2_name' AND LEVEL4_NAME='$level4_name' AND Production_Status='$production_status' AND Sample_Status='$sample_status' ORDER by colorstyle desc";
else
    $production_status = "production_incomplete";
    
    //$query_where = "WHERE LEVEL2_NAME='$level2_name' AND LEVEL4_NAME='$level4_name' AND Production_Status='$production_status' AND Sample_Status='$sample_status' ORDER by colorstyle desc";

    //$query = $query_select . $query_where;
//
/////////	
// Run Query and Set $result to the Result--MYSql Run Query	///
//
    $result = mysql_query($query);
//echo "$result";
//
///
//
if (!$result)
    die("Database access failed: " . mysql_error());
////
///
//
//
///////////////////////							///////////////
///////////												////////
/////////////											////////
//////////////											////////
///////////////											//////
/////////											/////////
/////////	Output Formatted $results of $query		///////////
/////////
////////////////////////////////////////////////////////////
////////////
$rows = mysql_num_rows($result);
echo $rows;
echo '<br /><b><u>Total Styles Found: </u></b>' . $rows . '<br />';

for ($j = 0; $j < $rows; ++$j) {
    $row = mysql_fetch_row($result);
    echo '<br /><b>Style: </b>' . $row[1] . '<br />';
    echo '<br /><b>Photo_Date: </b>' . $row[2] . '<br />';
    //echo '<br /><b>Brand: </b>' . $row[3] . '<br />';
    echo '<br /><b>Product_Type: </b>' . $row[5] . '<br />';
    echo '<br /><b>Product_Status: </b>' . $row[6] . '<br />';
    echo '<br /><b>Sample_Status: </b>' . $row[8] . '<br />';
}
////
///////
////////
////
///////
////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////																								////////////////																							////////////////
//////	Run any scripts set off by form passing arguments and optional values aka key:value pair	////////////////
//////																								////////////////
//////	////////////////////////		///////////////				//////////////////////////		////////////////
//////																										////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
///
////
///////
////////
///

if (isset($_POST['runscript']))
    $runscript = $_POST['runscript'];
	
if (isset($_POST['scriptargs']))
    $scriptargs = $_POST['scriptargs'];
	
$dorunscript   =	$runscript . '\ ' . $scriptargs;
	echo $dorunscript;
	
//////////////
//////////	
//	Compile Exiftag+value
//////////
if (isset($_POST['metatag']))
    $metatag = $_POST['metatag'];
    
if (isset($_POST['metavalue']))
    $metavalue = $_POST['metavalue'];

$exiftag   =	$metatag . '=' . $metavalue;
	echo $exiftag;
///    
////////	Compile 2nd submitted Exiftag 2+value
/////
///
if (isset($_POST['metatag2']))
    $metatag2 = $_POST['metatag2'];
    
if (isset($_POST['metavalue2']))
    $metavalue = $_POST['metavalue2'];

$exiftag2   =	$metatag2 . '=' . $metavalue2;
	echo $exiftag2;
        
?>
