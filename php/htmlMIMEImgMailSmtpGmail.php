<?php
	
	require_once "Mail.php";
	require_once "Mail/mime.php";
		//$from = "John Bragato <john.bragato@gmail.com>";
		//$to = "jbragato <jbragato@yahoo.com>";

    //change this to your email. 
    $to = "john.bragato@bluefly.com"; 
    $from = "john.bragato@gmail.com"; 
    $subject = "Hello! This is HTML email"; 
	$host = "ssl://smtp.gmail.com";
	$port = "465";
	$username = "john.bragato";
	$password = "yankee17";
	
	
    //begin of HTML message 
    $message = "<html> 
<body bgcolor=\"#DCEEFC\"> 
    <center> 
        <b>Looool!!! I am reciving HTML email......</b> <br> 
        <font color=\"red\">Thanks Mohammed!</font> <br> 
        <a href=\"http://www.gmail.com/\">* gmail.com</a> 
    </center> 
      <br><br>*** Now you Can send HTML Email <br> Regards<br>MOhammed Ahmed - Palestine 
  </body> 
</html>"; 
   //end of message 

    // To send the HTML mail we need to set the Content-type header. 
    //$headers = "MIME-Version: 1.0\r\n"; 
    //$headers .= "Content-type: text/html; charset: iso-8859-1\r\n"; 
    //$headers  .= "From: $from\r\n"; 
    //options to send to cc+bcc 
    //$headers .= "Cc: [email]maa@p-i-s.cXom[/email]"; 
    //$headers .= "Bcc: [email]email@gmail.com.cXom[/email]"; 
 	
	$mime = "1.0";
	$type = "text/html";
	$charset = "UTF-8";
	
	$headers = array ('From' => $from,
	          'To' => $to,
	          'Subject' => $subject,
			  'MIME-Version' => $mime,
			  'Content-type' => $type,
			  'Charset' => $charset);    

    // now lets send the email. 
    
	$smtp = Mail::factory('smtp',
		          array ('host' => $host,
		            'port' => $port,
		            'auth' => true,
		            'username' => $username,
		            'password' => $password));

		        $mail = $smtp->send($to, $headers, $message); 
	echo("$headers");
    echo "Message has been sent....!"; 

?>