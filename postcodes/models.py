from __future__ import unicode_literals

import re

from boundaries.models import Boundary
from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from django.utils.six.moves import reduce
from django.utils.encoding import python_2_unicode_compatible

Representative = None
Candidate = None
USE_CANDIDATES = False

try:
    from representatives.models import Representative
    from representatives.models import app_settings as representatives_settings
    from representatives.utils import boundary_url_to_name
    if getattr(representatives_settings, 'ENABLE_CANDIDATES', False):
        from representatives.models import Candidate
        USE_CANDIDATES = True
    USE_REPRESENTATIVES = True
except ImportError:
    USE_REPRESENTATIVES = False

r_postalcode = re.compile(r'^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]\d[ABCEGHJKLMNPRSTVWXYZ]\d$')


@python_2_unicode_compatible
class Postcode(models.Model):
    code = models.CharField(max_length=6, primary_key=True, validators=[RegexValidator(r_postalcode)])
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

    def __str__(self):
        return self.code

    def as_dict(self, sets=None):
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
        r.update(self.get_boundaries(sets=sets))
        if USE_REPRESENTATIVES:
            boundary_names = {}
            for match_type in ['concordance', 'centroid']:
                for boundary in r.get('boundaries_' + match_type, []):
                    boundary_names[boundary_url_to_name(boundary['url'])] = match_type
            if boundary_names:
                r.update(self.get_representatives(boundary_names, Representative))
                if USE_CANDIDATES:
                    r.update(self.get_representatives(boundary_names, Candidate))
        return r

    def get_boundaries(self, sets=None):
        r = {
            'boundaries_concordance': [],
            'boundaries_centroid': []
        }

        concordances = PostcodeConcordance.objects.filter(code=self.code).values_list('boundary', flat=True)

        if sets:
            concordances = filter(lambda b: b.split('/')[0] in sets, concordances)

        concordance_sets = set()

        if concordances:
            q = ((models.Q(set=concordance.split('/')[0]) & models.Q(slug=concordance.split('/')[1])) for concordance in concordances)

            boundaries = Boundary.objects.filter(reduce(lambda a, b: a | b, q))
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            boundaries = Boundary.get_dicts(boundaries)

            r['boundaries_concordance'] = boundaries

            for boundary in boundaries:
                concordance_sets.add(boundary['related']['boundary_set_url'])

        if self.centroid:
            q = models.Q(shape__contains=self.centroid)

            if sets:
                q &= models.Q(set__in=sets)

            boundaries = Boundary.objects.filter(q)
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            boundaries = Boundary.get_dicts(boundaries)

            r['boundaries_centroid'] = filter(lambda b: b['related']['boundary_set_url'] not in concordance_sets, boundaries)

        return r

    def get_representatives(self, boundary_names, model):
        if not USE_REPRESENTATIVES:
            raise NotImplementedError

        r = {}

        model_name = model._meta.verbose_name_plural

        for representative in model.objects.filter(boundary__in=boundary_names.keys()):
            key = model_name + '_' + boundary_names[representative.boundary]
            r.setdefault(key, []).append(representative.as_dict())

        return r


@python_2_unicode_compatible
class PostcodeConcordance(models.Model):
    code = models.ForeignKey(Postcode)
    boundary = models.TextField()
    source = models.CharField(max_length=30, help_text="A description of the data source.")

    class Meta:
        unique_together = (('code', 'boundary'))

    def __str__(self):
        return '%s -> %s' % (self.code_id, self.boundary)
