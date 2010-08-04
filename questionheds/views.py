import os
from django.conf import settings
from questionheds.models import Item
from questionheds.fetch import YahooNews
from django.http import Http404, HttpResponse
from django.views.generic.simple import direct_to_template


def index(request):
    """
    Returns a feed page with the latest items.
    """
    context = {
        'headline': u'Latest Questionheds',
        'feed_url': '/feeds/latest/',
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
    }
    template = 'feeds/index.html'
    return direct_to_template(request, template, context)


def fetch(request):
    """
    Fetch the latest data
    """
    start = request.GET.get('start', 1)
    yahoo = YahooNews(start)
    story_list = yahoo()
    adds = 0
    for item in story_list:
        query = Item.all()
        query = query.filter('title =', item['title'])
        if not query.fetch(1):
            obj = Item(
                title=item['title'],
                link=item['link'],
                description=item['description'],
                pubDate=item['pubDate'],
            )
            obj.put()
            adds += 1
    return HttpResponse('%s adds' % adds)


