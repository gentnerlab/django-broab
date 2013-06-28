django-neo
==========

Django package that implements the Python-Neo data model

Quick start
-----------

1. Add "neo" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'neo',
      )

2. Run `python manage.py syncdb` to create the polls models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create neo objects (you'll need the Admin app enabled).

4. Visit http://127.0.0.1:8000/admin/neo/ to view objects available.