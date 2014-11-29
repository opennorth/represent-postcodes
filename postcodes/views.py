from boundaries.base_views import APIView
from django.shortcuts import get_object_or_404

from postcodes.models import Postcode


class PostcodeDetailView(APIView):
    model = Postcode

    def get(self, request, code):
        postcode = get_object_or_404(Postcode, code=code)
        if request.GET.get('sets'):
            sets = request.GET['sets'].split(',')
        else:
            sets = None
        return postcode.as_dict(sets=sets)
