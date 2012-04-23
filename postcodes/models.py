import re

from django.contrib.gis.db import models
from django.core import urlresolvers
from django.core.validators import RegexValidator

from boundaries.models import Boundary
try:
    from representatives.models import Representative
    from representatives.utils import boundary_url_to_name
    USE_REPRESENTATIVES = True
except ImportError:
    Representative = None
    USE_REPRESENTATIVES = False

r_postalcode = re.compile(r'^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]\d[ABCEGHJKLMNPRSTVWXYZ]\d$')

class Postcode(models.Model):

    code = models.CharField(max_length=6, primary_key=True,
        validators=[RegexValidator(r_postalcode)])

    centroid = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=2, blank=True)

    objects = models.GeoManager()

    # @see http://en.wikipedia.org/wiki/List_of_postal_codes_in_Canada List of postal codes in Canada
    def save(self, *args, **kwargs):
        self.clean_fields()
        if not self.province:
            if self.code[0] == 'X':
                self.province = {
                    'X0A': 'NU',
                    'X0B': 'NU',
                    'X0C': 'NU',
                    'X0E': 'NT',
                    'X0G': 'NT',
                    'X1A': 'NT',
                }.get(self.code[0:3])
            else:
                self.province = {
                    'A': 'NL',
                    'B': 'NS',
                    'C': 'PE',
                    'E': 'NB',
                    'G': 'QC',
                    'H': 'QC',
                    'J': 'QC',
                    'K': 'ON',
                    'L': 'ON',
                    'M': 'ON',
                    'N': 'ON',
                    'P': 'ON',
                    'R': 'MB',
                    'S': 'SK',
                    'T': 'AB',
                    'V': 'BC',
                    'Y': 'YT',
                }.get(self.code[0])
        super(Postcode, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.code

    def as_dict(self):
        r = {
            'code': self.code,
            'city': self.city,
            'province': self.province,
        }
        if self.centroid:
            r['centroid'] = {
               'type': 'Point',
               'coordinates': [self.centroid.x, self.centroid.y]
            }
        r.update(self.get_boundaries())
        if USE_REPRESENTATIVES:
            for match_type in ['concordance', 'centroid']:
                reps = self.get_representatives(r.get('boundaries_' + match_type))
                if reps:
                    r['representatives_' + match_type] = reps
        return r

    def get_boundaries(self):
        r = {
            'boundaries_concordance': [],
            'boundaries_centroid': []
        }
        concordances = PostcodeConcordance.objects.filter(code=self.code).values_list('boundary', flat=True)
        concordance_sets = set()
        if concordances:
            q = ( (models.Q(set=c.split('/')[0]) & models.Q(slug=c.split('/')[1])) for c in concordances )
            boundaries = Boundary.objects.filter( reduce(lambda a,b: a | b, q) )
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            boundaries = Boundary.get_dicts(boundaries)
            for b in boundaries:
                concordance_sets.add(b['boundary_set_name'])
            r['boundaries_concordance'] = boundaries
        if self.centroid:
            boundaries = Boundary.objects.filter(shape__contains=self.centroid)
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            r['boundaries_centroid'] = filter(
                lambda b: b['boundary_set_name'] not in concordance_sets,
                Boundary.get_dicts(boundaries)
            )
        return r
        
    def get_representatives(self, boundaries):
        """Return a list of dicts matching the elected reps for the provided boundaries.
        
        The boundaries argument should be a list of dicts, as in boundaries_ keys in the
        postcode API response."""
        if not USE_REPRESENTATIVES:
            raise NotImplementedError
        if not boundaries:
            return []
        boundary_names = [boundary_url_to_name(b['url']) for b in boundaries]
        return [
            r.as_dict() for r in
            Representative.objects.filter(boundary__in=boundary_names)
        ]

class PostcodeConcordance(models.Model):

    code = models.ForeignKey(Postcode)
    boundary = models.TextField()
    source = models.CharField(max_length=30,
        help_text="An internal-use string referring to the source of this data.")

    class Meta:
        unique_together = (
            ('code', 'boundary')
        )

    def __unicode__(self):
        return u"%s -> %s" % (self.code_id, self.boundary)