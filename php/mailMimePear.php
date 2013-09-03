 <?php
	require_once "Mail.php";
	require_once "Mail/mime.php";
	//$from = "John Bragato <john.bragato@gmail.com>";
	//$to = "jbragato <jbragato@yahoo.com>";

	$from = "john.bragato@gmail.com";
	$recipient = "john.bragato@bluefly.com";
	$subject = "Hi!";
	$body = "Ciao,\n\tHow <b>are</b> you?";
	$replyto = "john.bragato@gmail.com";
	
	// Set up the headers that will be included in the email.
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
	
	// Read in the Html Email File       
	$htmlbody	=	shell_exec("cat " . "~/Dropbox/Dropbox_sites/Dreamweaver_sites/1test.html");
	$textbody	=	shell_exec("cat " . "~/Dropbox/Dropbox_sites/Dreamweaver_sites/1test.html");
	
	// Add the text and HTML versions as parts within the main email.
	$textmime = $email->addSubPart($textbody, $textparams);
	$htmlmime = $email->addSubPart($htmlbody, $htmlparams);
	       
	// Get back the body and headers from the MIME object. Merge the headers with
	// the ones we defined earlier.
	$final = $email->encode();
	$final['headers'] = array_merge($final['headers'], $headers);
	
	// Perform the actual send.
	$smtp_params = array();
	$smtp_params['host'] = 'ssl://smtp.gmail.com';
	$smtp_params['port'] = '465';
	$smtp_params['auth'] = true;
	$smtp_params['username'] = 'john.bragato';
	$smtp_params['password'] = 'yankee17';
	$smtp_params['persist'] = true;
	
	$mail =& Mail::factory('smtp', $smtp_params);
	$status = $mail->send($recipient, $final['headers'], $final['body']);
	echo $status;
?>