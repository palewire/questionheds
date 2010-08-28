# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Urls
from django.conf.urls.defaults import *

# Settings
from django.conf import settings

# Feeds
from questionheds.feeds import LatestHeds
from questionledes.feeds import LatestLedes

urlpatterns = patterns('',

    #url(r'^$', 'questionheds.views.index', name='index'),
    url(r'^$', 'django.views.generic.simple.redirect_to', 
        {'url': '/feeds/latest/'}, name='index'),

    url(r'^_/update/heds/$', 'questionheds.tasks.update_handler', name='update-hander'),
    url(r'^_/fetch/heds/$', 'questionheds.tasks.fetch_worker', name='fetch-worker'),

    url(r'^_/update/ledes/$', 'questionledes.tasks.update_handler', name='update-ledes-hander'),
    url(r'^_/fetch/ledes/$', 'questionledes.tasks.fetch_worker', name='fetch-ledes-worker'),
    url(r'^_/add/blacklist/lede/$', 'questionledes.tasks.add_blacklist_worker', name='add-blacklist-ledes-worker'),
    url(r'^_/add/blacklist/domain/$', 'questionledes.tasks.add_blacklist_domain_worker', name='add-blacklist-domain-worker'),

    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': dict(latest=LatestHeds, heds=LatestHeds, ledes=LatestLedes) }, name='feeds'),

)
