from questionheds.models import Item
from questionheds.fetch import YahooNews
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
            url=reverse('fetch-worker', args=[]),
            params=dict(start=start),
            method='GET'
        )
    return HttpResponse('Updating', mimetype='text/plain')


def fetch_worker(request):
    """
    Examine a YahooNews feed and figure out what records need to be added.
    """
    start = request.GET.get('start', 1)
    yahoo = YahooNews(start)
    story_list = yahoo()
    adds = 0
    for item in story_list:
        query = Item.all()
        query = query.filter('title =', item['title'])
        if not query.fetch(1):
            data = dict(
                title=item['title'],
                link=item['link'],
                description=item['description'],
                pubDate=item['pubDate'],
            )
            taskqueue.add(
                url=reverse('add-worker', args=[]),
                params=data,
                method='GET'
            )
            adds += 1
    return HttpResponse('%s adds' % adds, mimetype='text/plain')


def add_worker(request):
    """
    Adds a record to the Item model.
    """
    data = dict(
        title=request.GET.get('title'),
        link=request.GET.get('link'),
        description=request.GET.get('description'),
        pubDate=request.GET.get('pubDate'),
    )
    obj = Item(**data)
    obj.put()
    return HttpResponse(u"'%s' added" % data['title'], mimetype='text/plain')
