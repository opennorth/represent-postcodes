import csv
import logging
from optparse import make_option
import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.template.defaultfilters import slugify

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = """Imports a CSV file describing a concordance of postal codes
    to boundaries. Arguments:

boundary-set-slug: the slug of the BoundarySet the concordance is for
source: <= 30 characters describing where this concordance is from
filename: a two-column CSV file, where column 1 is the postcode and
    column 2 is a reference to the boundary (see the --searchfield option)

If no filename is provided, reads from STDIN."""
    args = '<boundary-set-slug> <source> [<filename>]'

    option_list = BaseCommand.option_list + (
        make_option('--searchfield', action='store', dest='search-field', default='external_id',
            help="Which Boundary field the second column of the CSV file corresponds to. Either 'external_id', 'name' or 'slug'. Default is external_id."),
    )

    @transaction.commit_on_success
    def handle(self, *args, **options):
        from postcodes.models import Postcode, PostcodeConcordance
        from boundaries.models import Boundary, BoundarySet

        if len(args) < 2:
            raise CommandError("boundary-set-slug and source arguments are required. See --help.")

        boundary_set_slug = args[0]
        source = args[1]

        try:
            filename = args[2]
            f = open(filename)
        except IndexError:
            f = sys.stdin

        # Delete all concordances from this source.
        PostcodeConcordance.objects.filter(source=source).delete()

        boundary_set = BoundarySet.objects.get(slug=boundary_set_slug)
        boundaries = Boundary.objects.filter(set=boundary_set)

        boundaries_seen = dict()
        for (code, searchterm) in csv.reader(f):
            try:
                (postcode, created) = Postcode.objects.get_or_create(code=code)
            except ValidationError as e:
                print "%s: %r" % (code, e)
                continue

            try:
                boundary = boundaries_seen.get(searchterm)
                if not boundary:
                    if options['search-field'] == 'name':
                        boundary = boundaries.get(slug=slugify(searchterm))
                    else:
                        boundary = boundaries.get(**{options['search-field']: searchterm})
                    boundaries_seen[searchterm] = boundary
            except Boundary.DoesNotExist:
                print "Cannot find boundary for %s" % searchterm
                continue

            boundary_name = u"%s/%s" % (boundary_set.slug, boundary.slug)
            if PostcodeConcordance.objects.filter(code=postcode, boundary=boundary_name).exists():
                print "Concordance already exists for %s -> %s" % (code, boundary_name)
                continue
                
            PostcodeConcordance.objects.create(
                code=postcode,
                boundary=boundary_name,
                source=source,
            )
