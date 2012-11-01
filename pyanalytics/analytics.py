import httplib
import urllib
import md5
import os

"""

    GenAPI - Analytics library

    Copyright (c) 2012 apitrary

"""

def send_data (host, api_url, token_auth, urlref):
    conn = httplib.HTTPConnection(host)
    visitor_idstring = md5.new(os.urandom(500)).hexdigest()
    visitor_id = visitor_idstring[:16]
    opts = {'idsite' : '1', #  Defines the Website ID being tracked
            'rec': '1', # Required to force the request to be recorded
            'urlref' :  urlref, # Full referrer URL - no funciona
            'action_name' : 'Validation page',
            '_id' : visitor_id, #no funciona
            'token_auth' : token_auth,
            }

        #headers = {'User-agent' : 'analytics'}
        # make request

        # Encode this data and generate the final URL
    data = urllib.urlencode(opts)
    print data
    conn.request('POST', u"%s?%s" % (api_url, data), headers={'User-Agent' : 'analyticspiwik'})

        #response = conn.getresponse(urllib2.urlopen(conn.request))
    response = conn.getresponse()
    response.read()
    print response.read()

    print response.status, response.reason
    conn.close()
    return response.read()

#        conn.close()

if __name__ == "__main__":
    analytics = send_data(
                          host='app1.dev.apitrary.net', # Url apitrary
                          api_url='http://app1.dev.apitrary.net/piwik/piwik.php', #Url Piwik setup
                          #_id='aaaa111122223333', # id user
                          urlref="http://yahoo.comj",
                          token_auth='1818f4d2511808845473978ff481ebe2' # User authentication API Piwik
                          )
    print analytics
