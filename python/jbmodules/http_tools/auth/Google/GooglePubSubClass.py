#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'


### PubSub Push Notifications Client
class GooglePubSubClient:
    def __init__(self, project_name=None, topic_name=None):
        from oauth2client import client as oauth2client
        self.PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
        self.oauth2client = oauth2client
        self.service = self.instantiate_pubsub_client()
        self.project_name = project_name
        self.topic_name = topic_name

    def instantiate_pubsub_client(self,httpobj=None):
        import httplib2
        from apiclient import discovery
        credentials = self.oauth2client.GoogleCredentials.get_application_default()
        if credentials.create_scoped_required():
            credentials = credentials.create_scoped(self.PUBSUB_SCOPES)
        if not httpobj:
            httpobj = httplib2.Http()
        credentials.authorize(httpobj)
        return discovery.build('pubsub', 'v1beta2', http=httpobj)

    def create_pubsub_subscription(self):
        # Only needed if you are using push delivery
        #push_endpoint = 'https://someproject.appspot.com/myhandler'
        # Create a POST body for the Pub/Sub request
        if not self.project_name:
            self.project_name = 'default'
        body = {
            # The name of the topic from which this subscription receives messages
            'topic': 'projects/{0}/topics/{1}'.format(self.project_name, self.topic_name)
            # Only needed if you are using push delivery
            # 'pushConfig': {
            #     'pushEndpoint': push_endpoint
            # }
        }
        _subscription = self.service.projects().subscriptions().create(name='projects/{0}/subscriptions/{1}'.format(self.project_name, self.topic_name), body=body).execute()
        print 'Created: %s' % _subscription.get('name')
        return _subscription

    def get_subscriptions_list(self):
        next_page_token = None
        _subscriptions = []
        while True:
            resp = self.service.projects().subscriptions().list(
                project='projects/{}'.format(self.project_name),
                pageToken=next_page_token).execute()
            # Process each subscription
            for subscription in resp['subscriptions']:
                print subscription['name']
                _subscriptions.append(subscription)
            next_page_token = resp.get('nextPageToken')
            if not next_page_token:
                #break
                return _subscriptions

    def pull_acknowledge_msg(self):
        import base64
        # You can fetch multiple messages with a single API call.
        batch_size = 100
        _subscription = 'projects/{0}/subscriptions/{1}'.format(self.project_name, self.topic_name)
        # Create a POST body for the Pub/Sub request
        body = {
            # Setting ReturnImmediately to false instructs the API to wait
            # to collect the message up to the size of MaxEvents, or until
            # the timeout.
            'returnImmediately': False,
            'maxMessages': batch_size,
        }

        msg_data = []
        while True:
            resp = self.service.projects().subscriptions().pull(subscription=_subscription,
                                                               body=body).execute(num_retries=3)
            received_messages = resp.get('receivedMessages')
            if received_messages is not None:
                ack_ids = []
                for received_message in received_messages:
                    pubsub_message = received_message.get('message')
                    if pubsub_message:
                        # Process messages
                        msg_data.append(base64.b64decode(str(pubsub_message.get('data'))))
                        # Get the message's ack ID
                        ack_ids.append(received_message.get('ackId'))

                # Create a POST body for the acknowledge request
                ack_body = {'ackIds': ack_ids}

                # Acknowledge the message.
                self.service.projects().subscriptions().acknowledge( subscription=_subscription, body=ack_body).execute()
                return msg_data, ack_ids


if __name__ == '__main__':
    pubsub_client = GooglePubSubClient()
