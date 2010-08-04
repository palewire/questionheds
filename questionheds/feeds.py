from questionheds.models import Item
from django.contrib.syndication.feeds import Feed


class LatestEntries(Feed):
    title = "Latest Questionheds"
    link = "/feeds/latest/"
    description = "The latest Questionheds across the wire."
    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'

    def items(self):
        return Item.all().order('-pubDate').fetch(25)
        
    def item_pubdate(self, item):
        return item.pubDate

