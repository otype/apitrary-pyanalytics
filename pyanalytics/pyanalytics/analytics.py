# -*- coding: utf-8 -*-
"""

    GenAPI - Analytics library

    Copyright (c) 2012 apitrary

"""
import httplib
import urllib
from tornado import httpclient, ioloop
from tornado.httpclient import HTTPRequest

PIWIK_SITE_ID = '1'
PIWIK_REC = '1'
PIWIK_HOST = 'app1.dev.apitrary.net'
PIWIK_API_URL = 'http://{}/piwik/piwik.php'.format(PIWIK_HOST)
GENAPI_TRACKING_HOST = 'http://pygenapi'
GENAPI_USER_AGENT = {'User-Agent': 'genapi analytics-piwik'}

def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body
    ioloop.IOLoop.instance().stop()


def piwik_opts(tracking_url, action_name):
    """
        Construct the Piwik Options hash
    """
    return {
        'idsite': PIWIK_SITE_ID,
        'rec': PIWIK_REC,
        'url': tracking_url,
        'action_name': action_name
    }


def send_data(piwik_api_url, tracking_url, action_name):
    """
        Send data to Piwik SYNCHRONOUSLY
    """
    # Open connection
    conn = httplib.HTTPConnection(piwik_host)

    # GET parameters:
    opts = piwik_opts(tracking_url=tracking_url, action_name=action_name)

    # Encode this data and generate request with the final URL
    data = urllib.urlencode(opts)
    conn.request('GET', u"%s?%s" % (piwik_api_url, data), headers=GENAPI_USER_AGENT)
    response = conn.getresponse()
    conn.close()
    print data, response.status, response.reason # Debug info
    return response.read()


def send_data_asynchronously(piwik_api_url, tracking_url, action_name):
    """
        NOT-BLOCKING (asynchronous) Piwik call
    """
    # Build options hash
    opts = piwik_opts(tracking_url=tracking_url, action_name=action_name)

    # Create async client
    http_client = httpclient.AsyncHTTPClient()

    # Encode this data and generate request with the final URL
    data = urllib.urlencode(opts)

    # Create the request object with the options hash and the url-encoded API Url + headers
    url = u"%s?%s" % (piwik_api_url, data)
    print url
    http_request = HTTPRequest(
        url=url,
        method='GET',
        headers=GENAPI_USER_AGENT
    )

    # Run the call
    http_client.fetch(request=http_request, callback=handle_request)
    ioloop.IOLoop.instance().start()
    return "OK"


def track_request(api_id, request=None, async=False):
    if request:
        # e.g. extract the request data like user-agent etc.
        pass

    tracking_url = '{}/{}'.format(GENAPI_TRACKING_HOST, api_id)
    if async:
        analytics = send_data_asynchronously(
            piwik_api_url=PIWIK_API_URL, # Piwik Analytics host name
            tracking_url=tracking_url, # Tracking URL
            action_name=api_id              # Identifier for the given API
        )
    else:
        analytics = send_data(
            piwik_api_url=PIWIK_API_URL, # Piwik Analytics host name
            tracking_url=tracking_url, # Tracking URL
            action_name=api_id              # Identifier for the given API
        )

    return analytics

if __name__ == "__main__":
    api_id = 'universalapi'

    # Send the analytics tracking data
    for i in range(1, 20):
        print "NUM: {}".format(i)
        print track_request(api_id=api_id, async=True)
