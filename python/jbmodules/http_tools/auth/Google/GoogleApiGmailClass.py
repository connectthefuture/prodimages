#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
installed_clientid = '442933852469-iokl3lqr7pg6uv8gn63d71rf6luri7kp.apps.googleusercontent.com'
installed_clientsecret = 'KqEszjWRIi_VJJeAcKMdkzvK'
installed_redirect = 'urn:ietf:wg:oauth:2.0:oob'
from googleapiclient import http,errors

class GoogleGmailClient:
    def __init__(self,user_id='me', to=None, subject='Automated', message_text=None, localdir=None, filename=None):
        self.user_id = user_id
        if to is not None:
            self.to = to
        else:
            self.to = 'john.bragato@gmail.com, john.bragato@bluefly.com'
        self.subject = subject
        self.message_text  = message_text
        self.localdir = localdir
        self.filename = filename
        self.scopes = [ 'https://mail.google.com/',
                        'https://www.googleapis.com/auth/gmail.modify',
                        'https://www.googleapis.com/auth/gmail.readonly',
                        'https://www.googleapis.com/auth/gmail.compose' ]
        self.service = self.instantiate_gmail_serviceAccount_bfly()
        self.message = self.create_message()

    def instantiate_gmail_serviceAccount_bfly(self):
        import httplib2
        from googleapiclient.discovery import build
        from oauth2client.client import SignedJwtAssertionCredentials
        serviceName = 'gmail'
        version = 'v1'
        api_key = 'AIzaSyD09iZ54he2CKlayiBmw9zvkVt7Z6HbSY4'
        client_email = '442933852469-mibsk7qkepe62njis1rv6gi1em0v011k@developer.gserviceaccount.com'
        client_id = '442933852469-mibsk7qkepe62njis1rv6gi1em0v011k.apps.googleusercontent.com'
        scope = self.scopes[0] #'https://www.googleapis.com/auth/gmail.modify'
        f = file('/root/bfly-gmail-privatekey.p12','rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(client_email, key, scope=scope)
        _http = httplib2.Http()
        _http = credentials.authorize(_http)
        self.service = build(serviceName, version, http=_http)
        return self.service


    def send_message(self):
        """Send an email message.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        try:
            _message = (self.service.users().messages().send(userId=self.user_id, body=self.message).execute())
            print 'Message Id: %s' % _message['id']
            return _message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


    def create_draft(self):
        """Create and insert a draft email. Print the returned draft's message and id.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        self.message: The body of the email message, including headers.

        Returns:
        Draft object, including draft id and message meta data.
        """

        try:
            _message = {'message': self.message}
            draft = self.service.users().drafts().create(userId=self.user_id, body=_message).execute()
            print 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message'])
            return draft
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


    def create_message(self):
        """Create a message for an email.
        Args:
        user_id: Email address of the user_id.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        _message = MIMEText(self.message_text)
        _message['to'] = self.to
        _message['from'] = self.user_id
        _message['subject'] = self.subject
        self.message = {'raw': base64.urlsafe_b64encode(_message.as_string())}
        return self.message


    def create_message_with_attachment(self):
        """Create a message for an email.
        Args:
        user_id: Email address of the user_id.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        localdir: The directory containing the file to be attached.
        filename: The name of the file to be attached.

        Returns:
        An object containing a base64url encoded email object.
        """
        import os
        _message = MIMEMultipart()
        _message['to'] = self.to
        _message['from'] = self.user_id
        _message['subject'] = self.subject

        msg = MIMEText(self.message_text)
        _message.attach(msg)

        path = os.path.join(self.localdir, self.filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=self.filename)
        _message.attach(msg)

        self.message = {'raw': base64.urlsafe_b64encode(_message.as_string())}
        return self.message




def send_an_email(to,message):
    c = GoogleGmailClient()
    c.message_text = message
    c.to = to
    c.create_message()
    ret = c.send_message()
    print ret
    return ret

def main():
    pass


if __name__ == '__main__':
    main()
