import os
import sys
import urllib
from django.conf import settings

# Date and text manipulation
from datetime import datetime
from django.utils import simplejson


class YahooNews(object):
    """
    A minimal YahooNews client. 
    """
    
    def __init__(self, start):
        self.APP_ID = settings.YAHOO_APP_ID
        self.start = start

    def __getattr__(self):
        return YahooNews()
        
    def __repr__(self):
        return "<YahooNews: %s>" % self.APP_ID
        
    def __call__(self):
        
        base_url = 'http://search.yahooapis.com/NewsSearchService/V1/newsSearch'
        params = dict(
            appid=self.APP_ID,
            start=self.start,
            query='?',
            results=50,
            language='en',
            output='json',
            sort='date',
        )
        url = '%s?%s' % (base_url, urllib.urlencode(params))
        response = urllib.urlopen(url)
        data = response.read()
        json = simplejson.loads(data)
        headline_list = [
            dict(
                title=i['Title'],
                link=i['Url'],
                description=i['Summary'],
                pubDate=datetime.fromtimestamp(float(i['PublishDate'])),
            ) for i in json['ResultSet']['Result']
                if i['Title'][-1] == '?'
        ]
        return headline_list



if __name__ == '__main__':
    update()
