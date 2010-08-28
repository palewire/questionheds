from google.appengine.ext import db


class LedeItem(db.Model):
    """
    A news story in RSS format
    """
    title = db.StringProperty()
    link = db.LinkProperty()
    domain = db.StringProperty()
    lede = db.StringProperty()
    description = db.TextProperty()
    pubDate = db.DateTimeProperty()

    def get_absolute_url(self):
        return self.link


class LedeBlacklist(db.Model):
    """
    Ledes we want to block.
    """
    lede = db.StringProperty()


class DomainBlacklist(db.Model):
    """
    Domains we want to block.
    """
    domain = db.StringProperty()
