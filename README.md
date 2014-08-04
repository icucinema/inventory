inventory
=========

The inventory module for cintranet.

This module is developed stand alone from cintranet, but it is expected to be used as part
of cintranet. If you want to just use this module on it's own, or as part of any other Django
project, that should be possible too.

The ```inventory_test``` folder included in this repo is a basic Django site to allow running this
module standalone to aid development.

Requirements
------------

* Python 2.7
* Django 1.6
* django-reversion 1.8
* south
* djangorestframework
* django-filter
* pillow

Development
-----------

The contents of this repository are a fully fledged Django site, ready to go for testing.
The app itself is in the ```inventory``` folder. The ```sitewide``` folder contains code lifted
from cintranet to make sure inventory app looks acceptable when running standalone, and the
```inventory_test``` folder is the Django site to allow for easy testing.

To get it up and running on your development machine, follow these steps.

1. Install the required dependencies.
2. Check out this repository somewhere.
3. Run ```python manage.py syncdb``` to set up the database.
4. Run ```python manage.py migrate``` to run the database migrations.
5. Run ```python manage.py runserver``` to launch the development web server.
6. Go to ```http://localhost:8000``` in your web browser, and let the fun begin.

Deployment
----------

1. Copy the ```inventory``` folder from within this repository to where your Django Apps are located.
2. Add ```inventory``` to the list of installed app in settings.py.
3. Run ```python manage.py migrate``` to add the database schema to the DB.
4. TODO: How to set up where images are stored.
5. TODO: How to get the static files in the right plaec.
6. TODO: Anything else required?


