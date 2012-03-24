from django.conf.urls.defaults import patterns, include, url

from postcodes.views import *

urlpatterns = patterns('',
    url(r'^postcodes/(?P<code>\w{6})/$', PostcodeDetailView.as_view()),
    url(r'^postcodes/(?P<code>\w{6})/boundaries/$', PostcodeBoundariesView.as_view(),
        name='postcode_boundaries'),
    url(r'^postcodes/(?P<code>\w{6})/representatives/$', PostcodeRepresentativesView.as_view(),
        name='postcode_representatives'),
)
