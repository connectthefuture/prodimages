<?php
require('../../conf/globals-3301.php');
$brand = $_GET['brand'];
		$gender = $_GET['gender'];
		$category = $_GET['category'];
		// Escape User Input to help prevent SQL Injection
		$ae_brand = mysql_real_escape_string($brand);
		$ae_gender = mysql_real_escape_string($gender);
		$ae_category = mysql_real_escape_string($category);
		
?>