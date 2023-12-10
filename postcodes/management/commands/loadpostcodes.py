import csv
import logging
import sys

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from postcodes.models import Postcode

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports a headerless CSV file with columns for code,latitude,longitude,locality,region. If no filename is given, reads from standard input.'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='?')

    def handle(self, *args, **options):
        if options['filename']:
            f = open(options['filename'])
        else:
            f = sys.stdin

        reader = csv.DictReader(f, fieldnames=['code', 'latitude', 'longitude', 'locality', 'region'])
        for row in reader:
            try:
                Postcode(
                    code=row['code'].upper(),
                    centroid=Point(float(row['longitude']), float(row['latitude'])),
                    city=row['locality'],
                    province=row['region'],
                ).save()
            except ValidationError as e:
                log.error("{}: {!r}".format(row['code'], e))
