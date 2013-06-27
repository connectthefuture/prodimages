 <?php
	require_once "Mail.php";
	require_once "Mail/mime.php";
	//$from = "John Bragato <john.bragato@gmail.com>";
	//$to = "jbragato <jbragato@yahoo.com>";

	if (isset($_POST['from'])) $from = $_POST['from'];
		else	$from = "john.bragato@gmail.com";
	
	if (isset($_POST['recipient'])) $recipient = $_POST['recipient'];
		else    $recipient = "(Not entered)";
			
	if (isset($_POST['subject'])) $subject = $_POST['subject'];
		else    $subject = "(Not entered)";
	
	if (isset($_POST['body'])) $body = $_POST['body'];
		else	$body = "(Not entered)";
		
	if (isset($_POST['replyto'])) $replyto = $_POST['replyto'];
		else	$replyto = "john.bragato@gmail.com";
		
	if (isset($_POST['filehtml'])) $filehtml = $_POST['filehtml'];
		else	$filehtml = "/mnt/Post_Ready/zProd_Server/imageServer7/mail/outbox/compiledPhotoReport.html";
	
	//$DAYRtmp = "date " . "+%Y-%m-%d-RetouchToDo";
	//$DAYRdo = shell_exec("$DAYRtmp");
	//$DAYR   =   "/mnt/Post_Ready/Daily/" . "$DAYRdo";
	//$filehtmlcount = shell_exec("`find /mnt/Post_Ready/Daily/$DAYR -type f | awk -F'/' '{ print $NF }' | sort | wc -l`");
	//$filehtmlcounttmp = "find " . "$DAYR";
	//$endoffilehtmlcounttmp = "-type " . "f " . "| " . "awk " . "-F'/' " . "'{ " .  "print " . "\$NF " . "}' " . "| " . "sort " . "| " . "wc " . "-l";
	//$filehtmlcount  =   "$filehtmlcounttmp" . "filehtmlcounttmp2";
	//$htmlsubject	=	shell_exec("$filehtmlcount");
	
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
	$htmlbody	=	shell_exec("cat " . "$filehtml");
	$textbody	=	shell_exec("cat " . "$filehtml");
	
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
