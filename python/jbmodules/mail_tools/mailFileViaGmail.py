#!/usr/bin/env python

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

import re,os,sys


gmail_user = "john.bragato@gmail.com"
gmail_pwd = ""

#for arg in sys.argv[1]:
#    print arg
#    toaddrs_list = []
#    pattern_email = re.compile(r'.+[@].+[.].+')
#    to_emailargs = re.findall(pattern_email, arg)
#    if to_emailargs:
#        for line in to_emailargs:
#            toaddrs_list.append(line)
#    else:
#        print "Fail"
#


## Test for HTML File is at sys.argv[3] to insert as Body of email
try:
	if sys.argv[2]:
		test = sys.argv[2]
		if os.path.isfile(test):
			bodyfile    = sys.argv[2]
			msgsubj     = "The Daily Completion Manifesto"
### Try to make body of message render HTML
			try:
				msgbody     = open(bodyfile, 'rb').read()
			except NameError:
				msgbody      = "NameErrorTestBody"
#                msgsubj      = "File: {0} was attached ByPython".format(os.path.basename(sys.argv[1]))
#                toaddrs      = "john.bragato@bluefly.com"
			if sys.argv[3]:
				toaddrs     = "john.bragato@bluefly.com"
			else:
				toaddrs     = "john.bragato@bluefly.com"
		else:
			toaddrs     = sys.argv[2]
			msgbody     = "TestBody"
			msgsubj     = "SentByPython"
except IndexError:
	toaddrs     = "john.bragato@bluefly.com"
	msgsubj    = "File: {0} was attached ByPython".format(os.path.basename(sys.argv[1]))
	msgbody     = "TestBody"

## Test for HTML File to insert as Body of email






## Include file as first arg as an attachment to mail
try:
	attachfile   = sys.argv[1]
	if os.path.isfile(attachfile):
		send_gmail(toaddrs, msgsubj, msgbody, attachfile)
	else:
		send_gmail(toaddrs, msgsubj, msgbody, "NotAfile")
except:
	print "Failed to Send File. Make Sure a valid file is your 1st Arg"
