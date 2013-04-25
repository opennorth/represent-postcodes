from django.shortcuts import get_object_or_404

from boundaries.base_views import APIView

from postcodes.models import Postcode

class PostcodeDetailView(APIView):

	model = Postcode

	def get(self, request, code):
		pc = get_object_or_404(Postcode, code=code)
		sets = request.GET['sets'].split(',') if request.GET.get('sets') else None
		return pc.as_dict(sets=sets)


