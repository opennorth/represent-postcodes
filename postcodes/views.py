from django.http import Http404
from django.shortcuts import get_object_or_404

from boundaries.base_views import ModelDetailView, ModelListView, APIView
try:
    from representatives.models import Representative
    from representatives.utils import boundary_url_to_name
    USE_REPRESENTATIVES = True
except ImportError:
    Representative = None
    USE_REPRESENTATIVES = False

from postcodes.models import Postcode

class PostcodeDetailView(ModelDetailView):

    model = Postcode

    def get_object(self, request, qs, code):
        return qs.get(code=code)

class PostcodeBoundariesView(APIView):
    model = Postcode

    def get(self, request, code):
        pc = get_object_or_404(Postcode, code=code)
        return pc.get_boundaries()

if USE_REPRESENTATIVES:
    class PostcodeRepresentativesView(APIView):
        model = Postcode

        def _get_reps(self, boundaries):
            boundary_names = [boundary_url_to_name(b['url']) for b in boundaries]
            if not boundary_names:
                return []
            return Representative.objects.filter(boundary__in=boundary_names)

        def get(self, request, code):
            pc = get_object_or_404(Postcode, code=code)
            boundaries = pc.get_boundaries()
            return {
                'representatives_centroid': [
                    r.as_dict() for r in
                    self._get_reps(boundaries['boundaries_centroid'])],
                'representatives_concordance': [
                    r.as_dict() for r in
                    self._get_reps(boundaries['boundaries_concordance'])],
            }

else:
    class PostcodeRepresentativesView(APIView):
        def get(self, *args, **kwargs):
            raise Http404

