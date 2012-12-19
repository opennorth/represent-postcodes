# Represent API: Postcodes

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected representatives and electoral districts. It provides a RESTful API to boundary, representative, and postcode resources.

This repository provides an API to postal codes. It depends on [represent-boundaries](http://github.com/rhymeswithcycle/represent-boundaries).

The [represent-canada](http://github.com/opennorth/represent-canada) repository provides a full sample app.

API documentation is available at [represent.opennorth.ca/api/](http://represent.opennorth.ca/api/#postcode).

## Adding data

Basic centroid information on postal codes comes courtesy of [geocoder.ca](http://geocoder.ca/?freedata=1). Load it with:

    python manage.py loadpostcodes

You can also load more accurate concordances between individual postal codes and boundaries. See:

    python manage.py loadpostcodeconcordance --help

## Contact

Please use [GitHub Issues](http://github.com/opennorth/represent-canada/issues) for bug reports. You can also contact represent@opennorth.ca.