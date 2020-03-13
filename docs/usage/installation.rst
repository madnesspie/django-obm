.. _installation:

Installation
============

.. role:: python(code)
   :language: python
.. role:: bash(code)
   :language: bash

Python package
--------------

.. code-block:: bash

    pip install django-cryptocurrency-framework

Django
------

Add packages in :python:`INSTALLED_APPS` in your :bash:`settings.py`::

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',

        'cc_framework.blockchain',
        'cc_framework.rest',  # if you need the REST API
    ]

If you specified :python:`cc_framework.rest` application update your :bash:`urls.py`::

    urlpatterns = [
        ...
        url(r'^cc_framework/', include('cc_framework.rest.urls')),
        ...
    ]

Post-Installation
-----------------

Migrate database
````````````````

In your Django root execute the command below to create your database tables::

    python manage.py migrate

Install nodes
`````````````

:bash:`django-cryptocurrency-framework` interact with blockchains through
cryptocurrency nodes so you should install and configure it. Now only
following nodes are being supported by the framework:

- Bitcoin: `bitcoin-core <https://bitcoincore.org/en/download/>`_
