from questionledes.models import LedeItem, LedeBlacklist
from questionledes.fetch import YahooNews
from google.appengine.api.labs import taskqueue
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse


def update_handler(request):
    """
    Schedule the latest fetches to be run.
    """
    # Loop through all the records
    for start in [1,51,101,151,201,251,301,351,401,451,501,551,601,651,701]:
        taskqueue.add(
            url=reverse('fetch-ledes-worker', args=[]),
            params=dict(start=start),
            method='GET'
        )
    return HttpResponse('Updating', mimetype='text/plain')


def add_blacklist_worker(request):
    """
    Add a new black list item.
    """
    lede = request.GET.get('lede', None)
    if not lede:
        raise Http404
    query = LedeBlacklist.all()
    query = query.filter('lede =', lede)
    if not query.fetch(1):
        obj = LedeBlacklist(lede=lede)
        obj.put()
    return HttpResponse('OK', mimetype='text/plain')


def fetch_worker(request):
    """
    Examine a YahooNews feed and figure out what records need to be added.
    """
    start = request.GET.get('start', 1)
    yahoo = YahooNews(start)
    story_list = yahoo()
    adds = 0
    for item in story_list:
        query = LedeItem.all()
        query = query.filter('title =', item['title'])
        if not query.fetch(1):
            data = dict(
                title=item['title'],
                link=item['link'],
                lede=item['lede'],
                description=item['description'],
                pubDate=item['pubDate'],
            )
            obj = LedeItem(**data)
            obj.put()
            adds += 1
    return HttpResponse('%s adds' % adds, mimetype='text/plain')

