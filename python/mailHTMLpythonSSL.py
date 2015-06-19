#!/usr/bin/env python3


def send_html_via_gmail(toaddr, subject=None, html_body=None, text_body=None):
    import smtplib, os.path

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    gmail_user = 'john.bragato@bluefly.com'  #str(input('Enter your Gmail or GoogleApps Address in single quotes: '))
    gmail_pass = open('/home/johnb/.gcreds.dat', 'rb').read()  #str(input('Enter your password in single quotes: '))

    toaddr = toaddr #"john.bragato@gmail.com,john.bragato@bluefly.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = toaddr
    if not subject:
        msg['Subject'] = str(len(text_body.splitlines())) + ' Lines Included'
    else:
        msg['Subject'] = subject

    # Create the body of the message (a plain-text and an HTML version).
    text = '\v'.join(text_body.split())
    html = """
    <html>
      <head>
            <link href"//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
            <link href"//cdn.datatables.net/plug-ins/1.10.7/integration/bootstrap/3/dataTables.bootstrap.css">
            <link href"//code.jquery.com/jquery-1.11.1.min.js">
            <link href"//cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js">
            <link href"//cdn.datatables.net/plug-ins/1.10.7/integration/bootstrap/3/dataTables.bootstrap.js">
      </head>
      <body>
      <strong>{0}</strong>
      <hr>
        {1}
      </body>
    </html>
    """.format(subject, html_body)

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
    server_ssl.sendmail(gmail_user, toaddr, msg)
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
        send_html_via_gmail(toaddr, subject=subject, html_body=content, text_body=subject)
    except IndexError:
        print('Please supply at least the to address and email content as arg 1 and 2, respectively.')
