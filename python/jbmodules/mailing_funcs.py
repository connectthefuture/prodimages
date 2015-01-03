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

def send_email_zerobyte_alerts(groupdict):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # me == my email address
    # you == recipient's email address
    from_addr = "john.bragato@gmail.com"
    to_addr = "john.bragato@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Failed Upload"
    msg['From']    = 'johnb@prodimages.ny.bluefly'
    msg['To']      = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Failed Files:\n\vPlease Reload the Following Styles:\n{0}".format(failed_styles)
    html = """\
    <html>
      <head></head>
      <body>
        <p>Failed Files<br>
           Please Reload the Following Styles:<br>
           {0}
        </p>
      </body>
    </html>
    """.format(failed_styles)

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
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    mailServer.sendmail(me, you, msg.as_string())
    mailServer.close()


def send_attachment_gmail(to, subject, text, attach):
    import smtplib, os
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    gmail_user = 'john.bragato@gmail.com'
    gmail_pass = ''
    msg = MIMEMultipart()
    msg['From']    = gmail_user
    msg['To']      = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pass)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()