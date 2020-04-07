.. _installation_page:

.. role:: python(code)
   :language: python
.. role:: bash(code)
   :language: bash

Installation
============

Python package
--------------

.. code-block:: bash

    pip install django-obm

Django
------

Add packages in :python:`INSTALLED_APPS` in your :bash:`settings.py`.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',

        'django_obm',
    ]

If you need the REST API for :bash:`django_obm` models, update your
:bash:`urls.py`.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^django_obm/', include('django_obm.urls')),
        ...
    ]

Post-Installation
-----------------

Migrate database
````````````````

In your Django root execute the command below to create your database tables:

.. code-block:: bash

    python manage.py migrate

.. _install-cryptocurrency-nodes:

Install cryptocurrency nodes
````````````````````````````

:bash:`django-obm` interact with blockchains through
cryptocurrency nodes. You should install them and allow RPC access.
Configuration example for each supported node is in
`example project <https://github.com/madnesspie/django-obm/tree/master/example>`_.

Now only following nodes are being supported by the framework:

- Bitcoin: `bitcoin-core <https://bitcoincore.org/en/download/>`_
