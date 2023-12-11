from django.urls import re_path

from postcodes.views import PostcodeDetailView

urlpatterns = [
    re_path(r'^postcodes/(?P<code>\w{6})/$', PostcodeDetailView.as_view()),

    # Backwards compatibility.
    re_path(r'^postcodes/(?P<code>\w{6})/boundaries/$', PostcodeDetailView.as_view()),
    re_path(r'^postcodes/(?P<code>\w{6})/representatives/$', PostcodeDetailView.as_view()),
]
