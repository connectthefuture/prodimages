<?php
		$db_local_hostname = "127.0.0.1:3306";
		$db_local_database = 'imageMetaData';
		$db_local_username = 'root';
		$db_local_password = 'root';
		
		// Socket Connect : $db_local_hostname = ":/Applications/MAMP/tmp/mysql/mysql.sock";
		//Connect to MySQL Server 
		$db_local_server = mysql_connect($db_local_hostname, $db_local_username, $db_local_password);
		if (!$db_local_server)
			die("Unable to connect to MySQL: " . mysql_error());

		//Select Database
		mysql_select_db($db_local_database) or die("Unable to select database: " . mysql_error());

		// Sanitize User Input of _POST data
		//echo "$db_local_database";
		
		
		
		// Get _POST array Data from Form input and Build Query
		
		if (isset($_POST['style'])) $style = $_POST['style'];
		else $style = "(Not entered)";
		
		if (isset($_POST['brand'])) $brand = $_POST['brand'];
		else	$brand = "(Not entered)";
		
		if (isset($_POST['level2_name'])) $level2_name = $_POST['level2_name'];
		else	$level2_name = "(Not entered)";
		
		if (isset($_POST['level4_name'])) $level4_name = $_POST['level4_name'];
		else	$level4_name = "(Not entered)";
		
		if (isset($_POST['production_status'])) $production_status = $_POST['production_status'];
		else	$production_status = "(Not entered)";
		
		if (isset($_POST['sample_status'])) $sample_status = $_POST['sample_status'];
		else	$sample_status = "(Not entered)";
		
		if (isset($_POST['qTable'])) $qTable = $_POST['qTable']; 
		else	$qTable = "(Not entered)";

		
		
		
		$query = "SELECT * FROM $qTable 
				WHERE level2_name='$level2_name' level4_name='$level4_name'
					AND Production_Status='$production_status' 
						OR Sample_Status='$sample_status'
							ORDER by COLORSTYLE desc";
		
			// WHERE COLORSTYLE='$style' AND Brand='$brand'";
		$result = mysql_query($query);
		//echo "$result";
		
		if (!$result) die("Database access failed: " . mysql_error());
		
		$rows = mysql_num_rows($result);
		//echo $rows;
		echo '<br /><b><u>Total Styles Found: </u></b>' .		$rows	. '<br />';
		
		for ($j = 0; $j < $rows; ++$j) 
		{
		$row = mysql_fetch_row($result);
		echo '<br /><b>Style: </b>' .					$row[0] . '<br />';
		echo '<br /><b>Brand: </b>' .					$row[1] . '<br />';
		echo '<br /><b>Product Type: </b>' .				$row[4] . '<br />';
		echo '<br /><b>Product Status: </b>' .				$row[5] . '<br />';
		}
		
?>