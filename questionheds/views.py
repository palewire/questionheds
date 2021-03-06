from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import RequestSite

def index(request):
    """
    Returns a feed page with the latest items.
    """
    context = {
        'headline': u'Questionheds',
        'feed_site': RequestSite(request),
        'feed_url': '/feeds/latest/',
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
    }
    template = 'feeds/index.html'
    return direct_to_template(request, template, context)



