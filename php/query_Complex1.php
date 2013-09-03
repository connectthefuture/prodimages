<!--
To change this template, choose Tools | Templates
and open the template in the editor.
-->
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title></title>
	</head>
	<body>
		<?php
		$db_local_hostname = "localhost:3306";
		$db_local_database = 'images_photoselects_jpg';
		$db_local_username = 'root';
		$db_local_password = 'root';
		//Connect to MySQL Server
		$db_local_server = mysql_connect($db_local_hostname, $db_local_username, $db_local_password);
		//Select Database
		mysql_select_db($db_local_database) or die(mysql_error());


		// Retrieve data from Query String
		$brand = $_GET['brand'];
		$gender = $_GET['gender'];
		$category = $_GET['category'];
		// Escape User Input to help prevent SQL Injection
		$ae_brand = mysql_real_escape_string($brand);
		$ae_gender = mysql_real_escape_string($gender);
		$ae_category = mysql_real_escape_string($category);



		//build query
		$query = "SELECT * FROM images WHERE ae_gender = '$gender'";
		if (is_numeric($brand))
			$query .= " AND ae_brand <= $brand";
		if (is_numeric($category))
			$query .= " AND ae_category <= $category";

		//Execute query
		$query_result = mysql_query($query) or die(mysql_error());

		//Build Result String
		$display_string = "<table>";
		$display_string .= "<tr>";
		$display_string .= "<th>Name</th>";
		$display_string .= "<th>brand</th>";
		$display_string .= "<th>gender</th>";
		$display_string .= "<th>category</th>";
		$display_string .= "</tr>";

		// Insert a new row in the table for each person returned
		while ($row = mysql_fetch_array($query_result)) {
			$display_string .= "<tr>";
			$display_string .= "<td>$row[ae_name]</>";
			$display_string .= "<td>$row[ae_gender]</td>";
			$display_string .= "<td>$row[ae_category]</td>";
			$display_string .= "</tr>";
		}

		echo "Query: " . $query . "<br />";
		$display_string .= "</table>";

		echo $display_string;

		mysql_close($db_local_server);
		?>
	</body>
</html>
