#!/usr/bin/env python
# -*- coding: utf-8 -*-

def download_email_attachments_by_label(email_address=None, email_password=None, gmail_label=None, keywordsSearch=None, mail_status=None, download_dir=None):
    import email, getpass, imaplib, os, datetime, json
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    ## Creds
    if not email_address:
        email_address  = 'john.bragato@bluefly.com'
        email_password = '0zeroseven'
    ### directory where to save attachments (default is current dir)
    if not download_dir:
        download_dir = '/home/johnb/virtualenvs/DJDAM/src/var/media/feeds'
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    ### Select the Keywords to search in mail and select the scope using gmail_label
    if not keywordsSearch:
        keywordsSearch = 'looklet'
    if not gmail_label:
        gmail_label = '1-PrimaryOps/Feeds'
    ## Choose UNSEEN messages or All including opened and seen messages
    if not mail_status:
        mail_status = 'UNSEEN'

    ## Login and Get mail box as m object, select by label etc
    m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    m.login(email_address, email_password)
    m.select(gmail_label)

    searchString = "(ALL SUBJECT '{0}')".format(keywordsSearch)
    resp, items = m.search(None, mail_status, searchString)
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
            attachment_dest = os.path.join(download_dir, today + "_" + filename)
            print attachment_dest
            if os.path.isfile(attachment_dest):
                os.remove(attachment_dest)
            fp = open(attachment_dest, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            return os.path.abspath(attachment_dest)


## Now that latest files have bee Downloaded - Get Delta of 2 most recent
def get_delta_from_json_file(filename=None, OLD_PATH=None, NEW_PATH=None, OUTPUT_DELTA_FILE=None, diffFilesDir=None):
    import difflib
    import os,re
    #regex_json = re.compile(r'^.+?.json$')
    #json_files = re.findall(regex_json, f)

    ## Define what we are diffing and were it is etc.
    if not filename:
        filename = 'LookletShotListImportJSON.json'
        diffFilesDir = '/home/johnb/virtualenvs/DJDAM/src/var/media/feeds'
    else:
        diffFilesDir = os.path.dirname(filename)

    if not OLD_PATH:
        OLD_PATH = os.path.join(diffFilesDir, filename)
        NEW_PATH = os.path.join(diffFilesDir, today + "_" + filename)
    if not NEW_PATH:
        NEW_PATH = os.path.join(diffFilesDir, today + "_" + filename)
    if not OUTPUT_DELTA_FILE:
        OUTPUT_DELTA_FILE =  os.path.join(diffFilesDir, today + "_" + "delta_file.txt")

    out = open(OUTPUT_DELTA_FILE, 'w')
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

    ## Rename the new file to the old file, eliminating the old file
    ## ie. updating the copy in the the directory
    os.rename(NEW_PATH, OLD_PATH)


def main():
    import sys, os, json, __builtin__
    try:
        filepath = sys.argv[1]
    except:
        filepath = download_email_attachments_by_label()
    if not os.path.isfile(filepath):
        filepath = download_email_attachments_by_label()
    if filepath.split('.')[-1] == 'json':
        try:
            json_data = json.load(__builtin__.open(filepath))
            return json_data
        except:
            print 'JSON couldnt be read Properly'
    else:
        try:
            get_delta_from_json_file(filepath)
        except:
            print 'Not A JSON File AND Delta could not be generated'


if __name__ == '__main__':
    main()
