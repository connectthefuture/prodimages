<?php

	require_once "Mail.php";
	require_once "Mail/mime.php";
	//$from = "John Bragato <john.bragato@gmail.com>";
	//$to = "jbragato <jbragato@yahoo.com>";

	        $from = "<john.bragato@gmail.com>";
	        $to = "<john.bragato@bluefly.com>";
	        $subject = "Hi!";
	        $body = "Ciao,\n\tHow <b>are</b> you?";
			
			//begin of HTML message 
			    $message = "<html> 
			<body bgcolor=\"#DCEEFC\"> 
			    <center> 
			        <b>Looool!!! <br><tab>I am reciving HTML email......</b> <br> 
			        <font color=\"red\">Thanks Mohammed!</font> <br> 
			        <a href=\"http://www.gmail.com/\">gmail.com</a> 
			    </center> 
			      <br><br>*** Now you Can send HTML Email <br> Regards<br>MOhammed Ahmed - Palestine 
			  </body> 
			</html>"; 
			   //end of message 

			$mime = "1.0";
			$type = "text/html";
	        $charset = "UTF-8";
			
			$host = "ssl://smtp.gmail.com";
	        $port = "465";
			$username = "john.bragato";
			$password = "yankee17";

	        $headers = array ('From' => $from,
	          'To' => $to,
	          'Subject' => $subject,
			  'MIME-Version' => $mime,
			  'Content-type' => $type,
			  'Charset' => $charset);
	        $smtp = Mail::factory('smtp',
	          array ('host' => $host,
	            'port' => $port,
	            'auth' => true,
	            'username' => $username,
	            'password' => $password));

	        $mail = $smtp->send($to, $headers, $message, $body);

	        if (PEAR::isError($mail)) {
	          echo("<p>" . $mail->getMessage() . "</p>");
	         } else {
	          echo("<p>Message successfully sent!</p>");
	         }

?>