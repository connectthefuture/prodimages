#!/usr/bin/env python
# -*- coding: utf-8 -*-



def send_text_via_gmail(toaddr, text=None, subject=None):
    import smtplib, os.path, email, __builtin__

    from email.mime.text import MIMEText
    from email import Encoders
    #print('Enter username or return to accept the default: \n')
    gmail_user = 'john.bragato@bluefly.com' #str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = open('/home/johnb/.gcreds.dat','rb').read() #str(input('Enter your password in single quotes: '))
    msg = MIMEText(text)
    msg['From']    = gmail_user
    msg['To']      = toaddr
    if not subject:
        msg['Subject'] = str(len(text.splitlines())) + ' Lines Included'
    else:
        msg['Subject'] = subject

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #mailServer.ehlo()
    mailServer.starttls()
    #mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    mailServer.sendmail(gmail_user, toaddr, msg.as_string())
    mailServer.quit()
    print(' Mail has been sent to %s' % toaddr)


if __name__ == '__main__':
    import sys
    subject = ''
    try:
        toaddr = str(sys.argv[1])
        if len(toaddr.split('@')) == 2:
            content = str(sys.argv[2])
            try:
                subject = sys.argv[3]
            except IndexError:
                pass
        else:
            content = toaddr
            toaddr  = 'john.bragato@gmail.com, john.bragato@bluefly.com' ## 'james.hoetker@bluefly.com', 'stephen.parker@bluefly.com']
            try:
                subject = sys.argv[2]
            except IndexError:
                pass
        send_text_via_gmail(toaddr, text=content, subject=subject)
    except IndexError:
        print('Please supply at least the to address and email content as arg 1 and 2, respectively.')

