#!/usr/bin/env python
# -*- coding: utf-8 -*-



def send_text_via_gmail(toaddr, text=None):
    import smtplib, os.path, email
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    #print('Enter username or return to accept the default: \n')
    gmail_user = str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = str(input('Enter your password in single quotes: '))
    msg = MIMEMultipart()
    msg['From']    = gmail_user
    msg['To']      = toaddr
    msg['Subject'] = str(len(text.split('\n'))), ' Records Included'

    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #mailServer.ehlo()
    mailServer.starttls()
    #mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    mailServer.sendmail(gmail_user, toaddr, msg)
    mailServer.quit()
    print(' Mail has been sent to %s' % toaddr)    

    
if __name__ == '__main__':
    import sys
    try:
        toaddr = sys.argv[1]
        content = sys.argv[2]
        send_text_via_gmail(toaddr, text=str(content).splitlines())
    except IndexError:
        print('Please supply the to address and email content as arg 1 and 2, respectively.')

