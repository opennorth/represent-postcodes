from boundaries.base_views import ModelDetailView

from postcodes.models import Postcode

class PostcodeDetailView(ModelDetailView):

    model = Postcode

    def get_object(self, request, qs, code):
        return qs.get(code=code)