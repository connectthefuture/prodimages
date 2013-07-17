#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


def send_gmail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

################# RUN ##################
import re,os


gmail_user = "john.bragato@gmail.com"
gmail_pwd = "yankee17"

for arg in sys.argv[0]:
    toaddrs_list = []
    pattern_email = re.compile(r'.+[@].+[.].+')
    to_emailargs = re.findall(pattern_email, arg)
    if to_emailargs:
        for line in to_emailargs:
        toaddrs_list.append(line)
    else:    
    
if len(toaddrs_list) = 0:
    toaddrs      = "john.bragato@bluefly.com"
elif len(toaddrs_list) = 1:
    toaddrs      = toaddrs_list.pop()
else:
    print toaddrs
#msgsubj     = sys.argv[2]
#bodyfile     = 
#msgbody     = open(bodyfile, 'rb').read()
#attachfile   = sys.argv[1]

#send_gmail("{toaddrs}".format(toaddrs="toaddrs"), "Hello from python!", "This is a email sent with <b>python</b>", attachfile)