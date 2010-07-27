# Views
from django.views.generic.simple import direct_to_template

HEADLINES = {
    'google': 'Trending on Google',
    'twitter': 'Trending on Twitter',
}

FEEDS = {
    'google': 'http://pipes.yahoo.com/pipes/pipe.run?_id=OtSAI5r83BGLeywRG8evXg&_render=rss',
    'twitter': 'http://pipes.yahoo.com/pipes/pipe.run?_id=bk_UedF43hGMQh2FqevxTA&_render=rss',
}


def index(request):
    """
    Returns a feed page, depending on the querystring.
    """
    slug = request.GET.get('feed', 'google')
    context = {
        'headline': HEADLINES[slug],
        'feed_url': FEEDS[slug],
    }
    template = 'feeds/index.html'
    return direct_to_template(request, template, context)
