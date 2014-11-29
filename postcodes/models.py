import re

from django.contrib.gis.db import models
from django.core.validators import RegexValidator

from boundaries.models import Boundary
Candidate = None
USE_CANDIDATES = False
try:
    from representatives.models import Representative
    from representatives.models import app_settings as rep_settings
    if getattr(rep_settings, 'ENABLE_CANDIDATES', False):
        from representatives.models import Candidate
        USE_CANDIDATES = True
    from representatives.utils import boundary_url_to_name
    USE_REPRESENTATIVES = True
except ImportError:
    Representative = None
    USE_REPRESENTATIVES = False

r_postalcode = re.compile(r'^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]\d[ABCEGHJKLMNPRSTVWXYZ]\d$')


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

    def __unicode__(self):
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
                for b in r.get('boundaries_' + match_type, []):
                    boundary_names[boundary_url_to_name(b['url'])] = match_type
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
        if sets:
            set_query = models.Q(set__in=sets)
        concordances = PostcodeConcordance.objects.filter(code=self.code).values_list('boundary', flat=True)
        if sets:
            concordances = filter(lambda b: b.split('/')[0] in sets, concordances)
        concordance_sets = set()
        if concordances:
            q = ((models.Q(set=c.split('/')[0]) & models.Q(slug=c.split('/')[1])) for c in concordances)
            boundaries = Boundary.objects.filter(reduce(lambda a, b: a | b, q))
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            boundaries = Boundary.get_dicts(boundaries)
            for b in boundaries:
                concordance_sets.add(b['related']['boundary_set_url'])
            r['boundaries_concordance'] = boundaries
        if self.centroid:
            boundary_query = models.Q(shape__contains=self.centroid)
            if sets:
                boundary_query = boundary_query & models.Q(set__in=sets)
            boundaries = Boundary.objects.filter(boundary_query)
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            r['boundaries_centroid'] = filter(
                lambda b: b['related']['boundary_set_url'] not in concordance_sets,
                Boundary.get_dicts(boundaries)
            )
        return r

    def get_representatives(self, boundary_names, model):
        """Return a dict of representatives of candidates for the provided boundaries.
        e.g. {
            'representatives_centroid': [ {}, {} ],
            'representatives_concordance': [ {} ]
        }

        - boundary_names: A dict of boundary names to match types,
            e.g. {'federal-electoral-districts/outremont': 'centroid'}
        - model: The Django model to query, either Representative or Candidate
        """
        if not USE_REPRESENTATIVES:
            raise NotImplementedError
        reps = model.objects.filter(boundary__in=boundary_names.keys())
        r = {}
        model_name = model._meta.verbose_name_plural
        for rep in reps:
            key = model_name + '_' + boundary_names[rep.boundary]
            r.setdefault(key, []).append(rep.as_dict())
        return r


class PostcodeConcordance(models.Model):
    code = models.ForeignKey(Postcode)
    boundary = models.TextField()
    source = models.CharField(max_length=30, help_text="An internal-use string referring to the source of this data.")

    class Meta:
        unique_together = (
            ('code', 'boundary')
        )

    def __unicode__(self):
        return u"%s -> %s" % (self.code_id, self.boundary)
