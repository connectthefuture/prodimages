<?php
	ob_start();
	phpinfo();
	$phpinfo = ob_get_contents();
	ob_end_clean();
	$answer = 'No';
		if (strpos($phpinfo, "") !== FALSE)
	{
    $answer = 'Yes';
	}
	echo $answer;
?>