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
    m.login('john.bragato@bluefly.com','forty000one')
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


def main():
    import email, imaplib, os, re
    regex_url = re.compile(r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/')
    regex_dbx = re.compile(r'(https://.+?[?]dl=0)')
    parsed = parse_gmail_mailbox_to_html_list()
    res = [ regex_dbx.findall(p) for p in parsed if p ]
    ret = sorted(list(set(sorted([l[0] for l in sorted(res)]))))
    
    return ret


if __name__ == '__main__':
    import requests
    ret = main()
    #for line in ret:
    #    r = requests.get(line).text.splitlines()
    print ret
