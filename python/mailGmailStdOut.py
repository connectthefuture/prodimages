#!/usr/bin/env python
# -*- coding: utf-8 -*-



def send_text_via_gmail(toaddr, text=None):
    import smtplib, os.path, email

    from email.MIMEBase import MIMEBase
    from email.mime.text import MIMEText
    from email import Encoders
    #print('Enter username or return to accept the default: \n')
    gmail_user = 'john.bragato@bluefly.com' #str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = '$cutler2377' #str(input('Enter your password in single quotes: '))
    msg = MIMEText(text)
    msg['From']    = gmail_user
    msg['To']      = toaddr
    msg['Subject'] = str(len(text.splitlines())) + ' Lines Included'


    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #mailServer.ehlo()
    mailServer.starttls()
    #mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    print(type(msg), type( msg.as_string()))
    mailServer.sendmail(gmail_user, toaddr, msg.as_string())
    mailServer.quit()
    print(' Mail has been sent to %s' % toaddr)    

    
if __name__ == '__main__':
    import sys
    try:
        toaddr = str(sys.argv[1])
        if len(toaddr.split('@')) == 2:
            content = str(sys.argv[2])
        else:
            content = toaddr
            toaddr  = 'john.bragato@gmail.com'
        send_text_via_gmail(toaddr, text=content)
    except IndexError:
        print('Please supply the to address and email content as arg 1 and 2, respectively.')

