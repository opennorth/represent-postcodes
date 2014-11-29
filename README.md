# Represent Postcodes

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected officials and electoral districts. It provides a [REST API](http://represent.opennorth.ca/api/) to boundary, representative, and postcode resources.

This repository provides an API to postal codes. API documentation is available at [represent.opennorth.ca/api/](http://represent.opennorth.ca/api/#postcode).

The [represent-canada](http://github.com/opennorth/represent-canada) repository provides a master Django project, and points to packages which add boundary, representative, and map features.

## Adding data

Load postal code centroids with:

    python manage.py loadpostcodes

Load postal code concordances with:

    python manage.py loadpostcodeconcordance --help

## Bugs? Questions?

This project's main repository is on GitHub: [http://github.com/rhymeswithcycle/represent-postcodes](http://github.com/rhymeswithcycle/represent-postcodes), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Released under the MIT license
