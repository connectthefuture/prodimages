<?php
	
// Instansiate POST data From HTML Form Setting Reply Address if available
	require_once('Mail.php');
//	require_once('/opt/local/lib/php/pear/Mail/mimePart.php');
//	require_once('/opt/local/lib/php/pear/Mail/sendmail.php');
	require_once('Mail/mime.php');
//	require_once('/opt/local/lib/php/pear/Mail/smtp.php');
	
	
	if(isset($_POST['mailfrom'])) $mailfrom   		= $_POST['mailfrom'];
	    else $mailfrom  =   "john.bragato@gmail.com";
	if(isset($_POST['mailto'])) $mailto   			= $_POST['mailto'];
         
//            else $mailto  =   "john.bragato@bluefly.com";
        
         else $mailto  =   "john.bragato@bluefly.com,stephen.parker@bluefly.com,jacqueline.wahba@bluefly.com,james.hoetker@bluefly.com,lydia.jeanlouis.temp@bluefly.com,conrad.sanderson@bluefly.com";
        
	if(isset($_POST['mailsubject'])) $mailsubject   = $_POST['mailsubject'];
        else $mailsubject  =   "The Lavender Report : Event's Incomplete Styles Statuses";
	if(isset($_POST['mailbody'])) $mailbody   		= $_POST['mailbody'];
        else $mailbody  =   "auto";
	
	$from 		= $mailfrom;
	$recipient 	= $mailto;
	$subject 	= $mailsubject;
	$body 		= $mailbody;
	
	if(isset($_POST['replyto'])) {	
		$replyto   = $_POST['replyto'];
	}
	else
	{
		$replyto = $from;
	}
		
	echo $from;

	echo $recipient;

	echo $replyto;
	
// Set up the headers array that will be included in the email.
	$headers = array(
	  'To'            => $recipient,
	  'From'          => $from,
	  'Return-Path'   => $from,
	  'Reply-To'      => $replyto,
	  'Subject'       => $subject,
	  'Errors-To'     => '<<a href="mailto:jbragato@yahoo.com">jbragato@yahoo.com</a>>',
	  'MIME-Version'  => '1.0',
	);
		
		
   	

// Set up parameters for both the HTML and plain text mime parts.
	$textparams = array(
		'charset'       => 'utf-8',
		'content_type'  => 'text/plain',
		'encoding'      => 'quoted/printable',
	  );
	
	$htmlparams = array(
		'charset'       => 'utf-8',
		'content_type'  => 'text/html',
		'encoding'      => 'quoted/printable',
	  );

	
	
	
	
	
// Create the email itself. The content is blank for now.
	$email = new Mail_mimePart('', array('content_type' => 'multipart/alternative'));
	
	
	// Read in the Html Email File using Shell Script      
	// if(isset($_POST['mailattach'])) {     	
// 		$attachment_raw   	= $_POST['mailattach'];
// 		//$attachment			= f
// 		$file_handle = fopen("$attachment_raw", "r");
// 
// 			while (!feof($file_handle)) {
// 
// 				$line = fgets($file_handle);
// 
// 				echo $line;
// 
// 			}
// 
// 			fclose($file_handle);
// 		
// 			$attachment = $file_handle;
// 		
// 		$htmlbody		= shell_exec("cat " . $attachment);
// 		$textbody		= shell_exec("cat " . $attachment);
// 	}
// 	//else
	//{
	//$htmlbody	= shell_exec("cat " . "~/Dropbox/Dropbox_sites/Dreamweaver_sites/1test.html");
	//$textbody	= shell_exec("cat " . "~/Dropbox/Dropbox_sites/Dreamweaver_sites/1test.html");
	//}

	$attachment = "/mnt/Post_Ready/zImages_1/dag/sites/queries_PHP-test1/Reports/event_incomplete_14days.html";
// 		
		$htmlbody		= shell_exec("cat " . $attachment);
 		$textbody		= shell_exec("cat " . $attachment);
	
// Add the text and HTML versions as parts within the main email.
	$textmime = $email->addSubPart($textbody, $textparams);
	$htmlmime = $email->addSubPart($htmlbody, $htmlparams);
	
	       
	// Get back the body and headers from the MIME object. Merge the headers with
	// the ones we defined earlier.
	$final = $email->encode();
	$final['headers'] = array_merge($final['headers'], $headers);
	
	


// SMTP Account Send Info 
	// Perform the actual send.
	$smtp_params = array();
	$smtp_params['host'] = 'ssl://smtp.gmail.com';
	$smtp_params['port'] = '465';
	$smtp_params['auth'] = true;
	$smtp_params['username'] = 'john.bragato@bluefly.com';
	$smtp_params['password'] = 'forty000One';
	$smtp_params['persist'] = true;
	
	$mail =& Mail::factory('smtp', $smtp_params);
	$status = $mail->send($recipient, $final['headers'], $final['body']);
	//echo $status;
	//echo $mail;



?>
