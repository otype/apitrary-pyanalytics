import httplib
import urllib

"""

    GenAPI - Analytics library

    Copyright (c) 2012 apitrary

"""

def send_data (urlref, action_name):
    host='app1.dev.apitrary.net' # Piwik hostname
    api_url='http://app1.dev.apitrary.net/piwik/piwik.php' # Url Piwik setup

    conn = httplib.HTTPConnection(host) # Open connection
    
    # GET parameters:
    opts = {'idsite' : '1', #  Defines the Website ID being tracked
               'rec': '1', # Required to force the request to be recorded
               'urlref' :  urlref,
               'action_name' : action_name 
               }

        # Encode this data and generate request with the final URL
    data = urllib.urlencode(opts)
    conn.request('GET', u"%s?%s" % (api_url, data), headers={'User-Agent' : 'genapi analytics-piwik'})
    response = conn.getresponse()
    conn.close()
    print data, response.status, response.reason # Debug info
    return response.read()

if __name__ == "__main__":
    analytics = send_data(
                         urlref="http://test.apitrary.com", # Full Referrer URL. Could be used as domain-id.
                         action_name='11111ru4gwydgb4v585h1nfmxjuyrt' # Page title. Could be used as api-id.
                  )
    print analytics