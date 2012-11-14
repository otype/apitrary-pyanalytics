# -*- coding: utf-8 -*-
"""

    GenAPI - Analytics library

    Copyright (c) 2012 apitrary

"""
import httplib
import urllib

def send_data(api_id, entity_name):
    host = '{}.dev.api.apitrary.com'.format(api_id)
    api_url = 'http://{}.dev.api.apitrary.com/{}'.format(api_id, entity_name)
    print api_url

    conn = httplib.HTTPConnection(host) # Open connection

    # GET parameters:
    opts = {
        'urlref': 'test',
        'action_name': 'test_action'
    }

    # Encode this data and generate request with the final URL
    data = urllib.urlencode(opts)
    conn.request('POST', u"%s?%s" % (api_url, data), headers={'User-Agent': 'genapi analytics-piwik'})
    response = conn.getresponse()
    conn.close()
    return data, response.status, response.reason, response.read()

if __name__ == "__main__":
    analytics = send_data(
        api_id='a8e29b20501846a7ba592f67b0accdaa',
        entity_name='requests'
    )
    print analytics