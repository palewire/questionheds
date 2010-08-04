from questionheds.models import Item
from questionheds.fetch import YahooNews


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
