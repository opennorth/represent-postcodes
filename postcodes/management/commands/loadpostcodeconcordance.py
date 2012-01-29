import csv
import logging
import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports a geocoder.ca postal code CSV file. Provide the filename as an argument.'

    option_list = BaseCommand.option_list + (
        # boundary-set
        # search-field
        # source
    )

    def handle(self, *args, **options):
        from postcodes.models import Postcode, PostcodeConcordance
        from boundaries.models import Boundary, BoundarySet
        try:
            filename = args[0]
            f = open(filename)
        except IndexError:
            f = sys.stdin

        bset = BoundarySet.objects.get(slug=options['boundary-set'])
        boundaries = Boundary.objects.filter(set=bset)

        boundaries_seen = dict()

        for (code, searchterm) in csv.reader(f):
            try:
                pc = Postcode.objects.get_or_create(code=code)
            except ValidationError as e:
                print "%s: %r" % (code, e)
                continue

            try:
                boundary = boundaries_seen.get(searchterm)
                if not boundary:
                    boundary = boundaries.get(**{
                        options['search-field']: searchterm
                    })
                    boundaries_seen[searchterm] = boundary
            except Boundary.DoesNotExist:
                print "Cannot find boundary for %s" % searchterm
                continue

            PostcodeConcordance.objects.create(
                code=pc,
                boundary=u"%s/%s" % (bset.slug, boundary.slug),
                source=options['source']
            )



