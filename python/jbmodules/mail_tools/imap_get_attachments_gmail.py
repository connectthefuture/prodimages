#!/usr/bin/env python
#import getpass, imaplib
#
#
#
#M = imaplib.IMAP4_SSL('imap.gmail.com')
#M.login('john.bragato@bluefly.com', 'ask')
#M.select()
##typ, data = M.search(None, 'ALL')
#typ, data = M.search(None, 'FROM', '"atgadmin@boapp201.l3.bluefly.com"')
#for num in data[0].split():
#        typ, data = M.fetch(num, '(RFC822)')
#        print 'Message %s\n%s\n' % (num, data[0][1])
#M.close()
#M.logout()

#####
import email, getpass, imaplib, os, datetime
dt = str(datetime.datetime.now())
today = dt.split(' ')[0]

### directory where to save attachments (default: current)

feeds_dir = '/mnt/Post_Complete/.Vendor_to_Load/feeds'
m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
m.login('john.bragato@bluefly.com','forty000One')
keywordsSearch = 'Feeds'
searchString = "(ALL SUBJECT '%s')" % keywordsSearch

### m.search(None, "(ALL SUBJECT 'bananas oranges')")
m.select('1-Consignment_Vendor-Imgs/FEEDS')
resp, items = m.search(None, searchString)
items = items[0].split()
for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)")
    email_body = data[0][1]
    mail = email.message_from_string(email_body)
    if mail.get_content_maintype() != 'multipart':
        continue
    print "["+mail["From"]+"] :" + mail["Subject"]
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        counter = 1
        if not filename:
            filename = 'part-%03d%s' % (counter, 'bin')
            counter += 1
        att_path = os.path.join(feeds_dir, today + "_" + filename)
        print att_path
        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

####
#IMAP_SERVER='imap.gmail.com'
#IMAP_PORT=993
#Gmail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
#rc, response = Gmail.login(username, password)
## Find the "All" messages in INBOX
#Gmail.select('FEEDS')
#typ, [response] = Gmail.search(None, 'ALL')
#if typ != 'OK':
#        raise RuntimeError(response)
## Create a new mailbox, "NewFolder"
#msg_ids = ','.join(response.split(' '))
#typ, create_response = Gmail.create('UPDATED_FEEDS')
#Gmail.copy(msg_ids, 'UPDATED_FEEDS')
## Look at the results
#Gmail.select('UPDATED_FEEDS')
#typ, [response] = Gmail.search(None, 'ALL')
#print 'COPIED:', response
#


#import imaplib
#mail = imaplib.IMAP4_SSL('imap.gmail.com')
#mail.login('john.bragato@gmail.com', '')
#mail.list()
# Out: list of "folders" aka labels in gmail.
#mail.select("inbox") # connect to inbox.
#lsm = mail.list()

#len(lsm)


#result, data = mail.uid('search', None, "ALL") # search and return uids instead
#latest_email_uid = data[0].split()[-1]
#result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
#raw_email = data[0][1]