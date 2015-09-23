#!/usr/bin/env python
# -*- coding: utf-8 -*-

def send_html_via_gmail(toaddr=None, subject=None, html_body=None, text_body=None):
    import smtplib, os.path

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    gmail_user = 'john.bragato@bluefly.com'  #str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = open('/home/johnb/.gcreds.dat', 'rb').read()  #str(input('Enter your password in single quotes: '))

    toaddr = toaddr.split() #"john.bragato@gmail.com,john.bragato@bluefly.com"
    print toaddr
    COMMASPACE = ', '

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = COMMASPACE.join(toaddr)
    if not subject:
        msg['Subject'] = str(len(text_body.splitlines())) + ' Lines Included'
    else:
        msg['Subject'] = subject

    # Create the body of the message (a plain-text and an HTML version).
    text = '\v'.join(text_body.split())
    html = """
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title><strong>{0}</strong></title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
        <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        <script src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
    </head>
    <body>
    <div class="container-fluid">
        <div class="table-responsive">
        {1}
        </div>

    </div>
    </body>
    </html>
    """.format(subject, html_body).replace('<TABLE BORDER=1>', '<table class="table table-striped">').replace('<TR>', '<tr><span class="glyphicon glyphicon-empty-star"></span>')

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via gmail secure SMTP Servers.
    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    #server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 587)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(gmail_user, gmail_pass)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(gmail_user, toaddr, msg.as_string())
    #server_ssl.quit()
    server_ssl.close()
    print 'successfully sent the mail: {0}'.format(subject)


    #s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(gmail_user, toaddr, msg.as_string())
    #s.quit()


if __name__ == '__main__':
    import sys
    subject = ''
    try:
        toaddr = str(sys.argv[1])
        print toaddr, ' <--- toaddr'
        if len(toaddr.split('@')) == 2:
            content = str(sys.argv[2])
            print len(toaddr.split('@')), '<-- len'
            try:
                subject = sys.argv[3]
            except IndexError:
                pass
        else:
            print len(toaddr.split('@')), '<-- lenElseOne'
            content = toaddr
            toaddr  = 'john.bragato@bluefly.com james.hoetker@bluefly.com stephen.parker@bluefly.com' #, sparker@udcny.com'
            try:
                subject = sys.argv[2]
            except IndexError:
                pass
        send_html_via_gmail(toaddr=toaddr, subject=subject, html_body=content, text_body=subject)
    except IndexError:
        print('Please supply at least the to address and email content as arg 1 and 2, respectively.')
