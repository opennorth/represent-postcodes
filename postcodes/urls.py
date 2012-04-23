from django.conf.urls.defaults import patterns, include, url

from postcodes.views import *

urlpatterns = patterns('',
    url(r'^postcodes/(?P<code>\w{6})/$', PostcodeDetailView.as_view()),
    
    # Our current plan is to have a single endpoint with all postcode data
    url(r'^postcodes/(?P<code>\w{6})/boundaries/$', PostcodeDetailView.as_view(),
        name='postcode_boundaries'),
    url(r'^postcodes/(?P<code>\w{6})/representatives/$', PostcodeDetailView.as_view(),
        name='postcode_representatives'),
)
