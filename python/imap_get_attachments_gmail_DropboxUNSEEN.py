#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_gmail_mailbox_to_html_list(mailbox_name=None,searchTerms=None):
    import imaplib, email, quopri
    if not mailbox_name:
        mailbox_name = '1-PrimaryOps/Dropbox-VendorLinks'
    else: pass
    if not searchTerms:
        searchTerms = '?dl=0'
    else: pass
    m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    m.login('john.bragato@bluefly.com','forty000One')
    searchString = "(ALL TEXT '{0}')".format(searchTerms)
    m.select(mailbox_name)
    #### Logged in and Mbox selected
    result, uidsAll = m.search(None, searchString)
    uidsAll = uidsAll[0].split() # search and return uids instead
    parsed_emails_list = []
    for emailid in uidsAll:
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)    
        raw_email = data[0][1]
        raw_email_decoded = str(quopri.decodestring(str(raw_email))).replace('\r\n',' ').strip(' ')
        parsed_emails_list.append(raw_email_decoded)
    m.logout()
    return parsed_emails_list


def parse_email_list_by_tag(parsed_email_aslist,tag_name=None):
    from bs4 import BeautifulSoup
    import codecs, re
    regex_url = re.compile(r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/')
    regex_dbx = re.compile(r'"(https://.+?[?]dl=1)"')
    if not tag_name:
        tag_name = 'div'
    soup = BeautifulSoup(parsed_email_aslist)
    divs = soup.findAll(tag_name)
    return divs ## list(set(sorted(divs)))


def download_file_url(url, localpath=None):
    import requests, os, io
    if localpath and os.path.isdir(localpath):
        localpath = os.path.join(localpath, url.split('/')[-1])
    res = requests.get(url, stream=True, timeout=1)
    with io.open(localpath, 'ab+') as f:
        f.write(res.content)
        f.close()
    return localpath


def unzip_dir_savefiles(zipin, extractdir):
    import zipfile,sys,datetime,os,re,io
    regex_png = re.compile(r'^[^\.].+?[png]{3}$')
    os.chdir(extractdir)
    # Open zip file
    zipf   = zipfile.ZipFile(zipin, 'r')
    
    # ZipFile.read returns the bytes contained in named file
    filenames = zipf.namelist()
    #print "777e3e3",os.path.abspath(os.curdir)
    for filename in filenames:
        if re.findall(regex_png, filename):    
            f = zipf.open(filename)
            contents = f.read()
            f.close()
            writefile = os.path.join(extractdir, filename.split('/')[-1])
            try:
                with io.open(writefile, 'w') as wfile:
                    wfile.write(contents)
                    print 'Extracting to --> {0}/{1}'.format(extractdir, filename.split('/')[-1])
            except IOError:
                print "IO Error -->{0}".format(filename)
                #os.rename(filename, filename.replace('2_Returned', 'X_Errors'))
                pass
    return zipin


def main(mailbox_name=None,searchTerms=None):
    import email, imaplib, os, re, requests
    regex_url = re.compile(r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/')
    regex_dbx = re.compile(r'(https://.+?[?]dl=0)')
    parsed = parse_gmail_mailbox_to_html_list(mailbox_name=mailbox_name,searchTerms=searchTerms)
    res = [ regex_dbx.findall(p) for p in parsed if p ]
    ret = sorted(list(set(sorted([l[0] for l in sorted(res)]))))
    
    ## Links to zips need to be downloaded\
    extractdir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
    if os.path.isdir(extractdir):
        pass
    else:
        extractdir = os.path.join(os.path.abspath('~'), 'Pictures', 'emailParserDownloads')
        if not os.path.isdir(extractdir):
            os.makedirs(extractdir, 16877)
        else: pass
    zip_downloads = [ download_file_url(url, localpath=extractdir) for url in ret if url ]

    ## Unzip Files
    zips_extracted = [ unzip_dir_savefiles(z,extractdir) for z in zip_downloads]

    return ret


if __name__ == '__main__':
    import requests
    ret = main()
    #for line in ret:
    #    r = requests.get(line).text.splitlines()
    print ret
