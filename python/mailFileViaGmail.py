#!/usr/bin/env python
# -*- coding: utf-8 -*-

def failed_upload_alerts(infile):
    import os,re
    regex_match_userstylealt_fail = re.compile(r'^(?:.*?/.*?originated_in_)(?P<firstname>[A-Z][a-z]+?)(?P<lastname>[A-Z][a-z]+?)/(?P<colorstyle>\d{9})(?P<alt>.*?)?(?:\.\w{2,4})$')
    matches = regex_match_userstylealt_fail.match(infile)
    if not matches:
        pass
    elif matches:
        groups     = matches.groupdict()
        filepath   = matches.string
        firstname  = groups['firstname']
        lastname    = groups['lastname']
        colorstyle = groups['colorstyle']
        alt        = groups['alt']
        email_addr = firstname.lower() + '.' + lastname.lower() + '@bluefly.com'
        return locals()

def send_email_zerobyte_alerts(groupeddict=None,gmail_user=None,gmail_pass=None):
    import smtplib, email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    firstname  = groupeddict['firstname']
    lastname   = groupeddict['lastname']
    colorstyle = groupeddict['colorstyle']
    alt        = groupeddict['alt']
    email_addr = groupeddict['email_addr']
    filepath   = groupeddict['email_addr']
    # me == my email address
    # you == recipient's email address
    from_addr = str(input('Enter your Gmail or GoogleApps Address: '))
    toaddr = email_addr

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Failed Upload " + colorstyle
    msg['From']    = from_addr
    msg['To']      = toaddr

    # Create the body of the message (a plain-text and an HTML version).
    text = "Failed Files:\n\vPlease Reload the Following Files:\n{0}".format(filepath.replace('/mnt/','/Volumes/'))
    html = """\
    <html>
      <head></head>
      <body>
        <p>Failed Files<br>
           Please Reload the Images: <a href='/Volumes/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/zero_byte_errors'> ZeroByteDir</a><br>
           <table><a href='{0}'> {1}</a></table>
        </p>
      </body>
    </html>
    """.format(filepath.replace('/mnt/','/Volumes/'),colorstyle)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    mailServer.sendmail(from_addr, toaddr, msg.as_string())
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    mailServer.close()


def send_attachment_gmail(toaddr, attach, subject=' -- File Attached -- ', text='Please save the attachement and open file locally.'):
    import smtplib, os.path, email, sys
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    #print('Enter username or return to accept the default: \n')
    if len(sys.argv) == 1:
        gmail_user = 'john.bragato@gmail.com'
    else:
        gmail_user = str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = open('/home/johnb/.gcreds.dat','rb').read() ##str(input('Enter your password in single quotes: '))
    msg = MIMEMultipart()
    msg['From']    = gmail_user
    msg['To']      = toaddr

    msg.attach(MIMEText(text))
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)
    msg['Subject'] = 'Filesize: ' + str(len(open(attach, 'rb').read())) + subject + ' Filename %s ' % os.path.basename(attach)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #mailServer.ehlo()
    mailServer.starttls()
    #mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    mailServer.sendmail(gmail_user, toaddr, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.quit()
    print "Mail with attachment {} \nSent to: {}".format(attach, toaddr)
    return


if __name__ == '__main__':
    import sys, os.path
    try:
        if len(sys.argv[0]) == 2:
            toaddr = sys.argv[1]
            attachment = sys.argv[2]
        else:
            toaddr = 'john.bragato@gmail.com'
            attachment = sys.argv[1]
        send_attachment_gmail(toaddr, os.path.abspath(attachment))
    except IndexError:
        print('Please supply the to address and the path to your attachment as arg 1 and 2, respectively.')

