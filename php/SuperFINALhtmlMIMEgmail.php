<?php

	include('Mail.php');
	include('Mail/mime.php');
	include('Mail/mimeDecode.php');
	$message = '<html><body>';
	$message .= '<img src="/Users/JCut/Dropbox/Dropbox_sites/imageServertmp/images/images_jpg_PhotoSelects/3151/315111401/315111401_1.jpg" alt="Test Image Display" width="200" />';
	$message .= '<table rules="all" style="border-color: #666;" cellpadding="10">';
	$message .= "<tr style='background: #eee;'><td><strong>Name:</strong> </td><td>" . strip_tags($_POST['req-name']) . "</td></tr>";
	$message .= "<tr><td><strong>Email:</strong> </td><td>" . strip_tags($_POST['req-email']) . "</td></tr>";
	$message .= "<tr><td><strong>Type of Change:</strong> </td><td>" . strip_tags($_POST['typeOfChange']) . "</td></tr>";
	$message .= "<tr><td><strong>Urgency:</strong> </td><td>" . strip_tags($_POST['urgency']) . "</td></tr>";
	$message .= "<tr><td><strong>URL To Change (main):</strong> </td><td>" . $_POST['URL-main'] . "</td></tr>";
	$addURLS = $_POST['addURLS'];
	if (($addURLS) != '') {
	    $message .= "<tr><td><strong>URL To Change (additional):</strong> </td><td>" . strip_tags($addURLS) . "</td></tr>";
	}
	$curText = htmlentities($_POST['curText']);           
	if (($curText) != '') {
	    $message .= "<tr><td><strong>CURRENT Content:</strong> </td><td>" . $curText . "</td></tr>";
	}
	$message .= "<tr><td><strong>NEW Content:</strong> </td><td>" . htmlentities($_POST['newText']) . "</td></tr>";
	$message .= "</table>";
	$message .= "</body></html>";

	echo($message);
	
	$text = 'Hello,\nHow are you doing?';
	$html = "$message";
	 
	$smtpinfo["host"] = "ssl://smtp.gmail.com";
	$smtpinfo["port"] = "465";
	$smtpinfo["auth"] = true;
	$smtpinfo["username"] = "john.bragato";
	$smtpinfo["password"] = "yankee17";
	 
	$recipients = "john.bragato@bluefly.com";
	$headers["From"] = "<john.bragato@gmail.com>";
	$headers["To"] = "<john.bragato@bluefly.com>";
	$headers["Subject"] = "Ciao Giancarlo!";
	 
	$mime = new mail_mime();
	$mime->setTXTBody($text);
	$mime->setHTMLBody($html);
	 
	$body = $mime->get();
	$headers = $mime->headers($headers);
	
	$mail =& Mail::factory('smtp', $smtpinfo);
	$mail->send($recipients, $headers, $body);
	 
	if(PEAR::isError($mail)){
	echo("
	 
	There was an error: " . $mail->getMessage() . "
	 
	");
	}else {
	echo("
	 
	Message Sent To
	 
	");
	}
?>