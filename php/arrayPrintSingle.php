
<?php

	/** Prints the contents of an array with HTML special characters, linebreaks and spaces
	* @param array $array
	* @param bool $echo (default: true)
	* @result bool/array
	*/
	function print_arr($array, $echo = true)
	{
	$array = print_r($array, true);
	$array = htmlspecialchars($array);
	$array = str_replace(" ", " ", $array);
	$array = nl2br("”.$array.”");

	if($echo == true)
	{
	echo $array;
	return true;
	}

	return $array;
	}
	
	# use like this to print/echo the contents to the screen
	//print_arr($yourArray);

	# use like this to not print/echo but catch the contents in a variable
	$result = $print_arr($yourArray);

?>
