import re
import os
import sys
import urllib
from django.conf import settings

# Date and text manipulation
from urllib2 import urlparse
from datetime import datetime
from django.utils import simplejson

# Models
from questionledes.models import LedeBlacklist
from questionledes.models import DomainBlacklist


class YahooNews(object):
    """
    A minimal YahooNews client. 
    """
    
    def __init__(self, start):
        self.APP_ID = settings.YAHOO_APP_ID
        self.start = start
        self.regex = re.compile('[.?!] [A-Z]')

    def __getattr__(self):
        return YahooNews()
        
    def __repr__(self):
        return "<YahooNews: %s>" % self.APP_ID
        
    def detect_questionlede(self, string):
        lede = self.get_lede(string)
        if not lede or lede[-1] != '?':
            return False
        query = LedeBlacklist.all()
        query = query.filter('lede =', lede)
        if query.fetch(1):
            return False
        return True

    def get_lede(self, string):
        search = self.regex.search(string)
        if not search:
            return None
        index = search.start()+1
        return string[:index]

    def get_domain(self, string):
        parts = urlparse.urlparse(string)
        return parts[1]

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
                domain=self.get_domain(i['Url']),
                lede=self.get_lede(i['Summary']),
                description=i['Summary'],
                pubDate=datetime.fromtimestamp(float(i['PublishDate'])),
            ) for i in json['ResultSet']['Result']
                if self.detect_questionlede(i['Summary'])
        ]
        # Filter out any black list domains
        final_list = []
        for i, hed in enumerate(headline_list):
            blacklist = DomainBlacklist.all()
            query = blacklist.filter('domain =', hed['domain'])
            if query.fetch(1):
                pass
            else:
                final_list.append(hed)
        # Return what's left
        return final_list


