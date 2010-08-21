from questionheds.models import HedItem
from django.contrib.syndication.feeds import Feed


class LatestHeds(Feed):
    title = "Latest Questionheds"
    link = "/feeds/latest/"
    description = "The latest Questionheds across the wire."
    title_template = 'feeds/heds/title.html'
    description_template = 'feeds/heds/description.html'

    def items(self):
        return HedItem.all().order('-pubDate').fetch(25)
        
    def item_pubdate(self, item):
        return item.pubDate

