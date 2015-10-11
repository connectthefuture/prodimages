#!/usr/bin/env python
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
resp, items = m.search(None, 'UNSEEN', searchString)
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


## Now that latest files have bee Downloaded - Get Delta of 2 most recent
import difflib
import os,re

regex = re.compile(r'.+?/[0-9]{4}-[0-9]{2}-[0-9]{2}_.+?.csv$')
feeds_files = os.listdir(feeds_dir)

for f in feeds_files:
    if re.findall(regex, f):
        print f

OLD_PATH = os.path.join(feeds_dir,'/mnt/Post_Complete/.Vendor_to_Load/feeds/sku-conv.csv')
NEW_PATH = os.path.join(feeds_dir, today + "_" + "sku-conv.csv")


outfile =  os.path.join(feeds_dir, today + "_" + "delta_file.txt")
out = open(outfile, 'w')
#
old = open(OLD_PATH, 'r')
old_lines = list(old)
print len(old_lines)
old.close()
#
new = open(NEW_PATH, 'r')
new_lines = list(new)
print len(new_lines)
new.close()
#
for line in difflib.unified_diff(old_lines, new_lines, fromfile=OLD_PATH, tofile=NEW_PATH):
    out.write(line)
    #print("Writter")


os.rename(NEW_PATH, OLD_PATH)
