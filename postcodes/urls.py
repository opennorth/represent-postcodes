from django.conf.urls.defaults import patterns, include, url

from postcodes.views import *

urlpatterns = patterns('',
    url(r'^postcodes/(?P<code>\w{6})/$', PostcodeDetailView.as_view()),
)
