import re

from django.contrib.gis.db import models
from django.core.validators import RegexValidator

from boundaries.models import Boundary

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
            if self.code[0] == 'X'
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
            'province': self.province
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
            r['centroid'] = {
               'type': 'Point',
               'coordinates': [self.centroid.x, self.centroid.y]
            }
            boundaries = Boundary.objects.filter(shape__contains=self.centroid)
            boundaries = Boundary.prepare_queryset_for_get_dicts(boundaries)
            r['boundaries_centroid'] = filter(
                lambda b: b['boundary_set_name'] not in concordance_sets,
                Boundary.get_dicts(boundaries)
            )

        return r

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