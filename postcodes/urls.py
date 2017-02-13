from django.conf.urls import url

from postcodes.views import PostcodeDetailView

urlpatterns = [
    url(r'^postcodes/(?P<code>\w{6})/$', PostcodeDetailView.as_view()),

    # Backwards compatibility.
    url(r'^postcodes/(?P<code>\w{6})/boundaries/$', PostcodeDetailView.as_view()),
    url(r'^postcodes/(?P<code>\w{6})/representatives/$', PostcodeDetailView.as_view()),
]
