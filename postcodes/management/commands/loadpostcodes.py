import csv
import logging
import sys

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports a geocoder.ca postal code CSV file. Expects either the filename as an argument, or to read the file over stdin.'

    def handle(self, *args, **options):
        from postcodes.models import Postcode
        try:
            filename = args[0]
            f = open(filename)
        except IndexError:
            f = sys.stdin

        reader = csv.DictReader(f, fieldnames=['code', 'lat', 'lng', 'city', 'province'])
        for line in reader:
            try:
                Postcode(
                    code=line['code'].upper(),
                    centroid=Point(float(line['lng']), float(line['lat'])),
                    city=line['city'].decode('iso-8859-1'),
                    province=line['province']
                ).save()
            except ValidationError as e:
                print "%s: %r" % (line['code'], e)

