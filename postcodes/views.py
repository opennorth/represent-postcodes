from django.http import Http404
from django.shortcuts import get_object_or_404

from boundaries.base_views import ModelDetailView, ModelListView, APIView

from postcodes.models import Postcode

class PostcodeDetailView(ModelDetailView):

    model = Postcode

    def get_object(self, request, qs, code):
        return qs.get(code=code)

