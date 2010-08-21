from questionledes.models import LedeItem
from django.contrib.syndication.feeds import Feed


class LatestLedes(Feed):
    title = "Latest Questionledes"
    link = "/feeds/latest/ledes/"
    description = "The latest Questionledes across the wire."
    title_template = 'feeds/ledes/title.html'
    description_template = 'feeds/ledes/description.html'

    def items(self):
        return LedeItem.all().order('-pubDate').fetch(25)
        
    def item_pubdate(self, item):
        return item.pubDate

