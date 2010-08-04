from google.appengine.ext import db


class Item(db.Model):
    """
    A news story in RSS format
    """
    title = db.StringProperty()
    link = db.LinkProperty()
    description = db.TextProperty()
    pubDate = db.DateTimeProperty()

    def get_absolute_url(self):
        return self.link

