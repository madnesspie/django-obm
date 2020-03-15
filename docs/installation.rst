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

    pip install django-cryptocurrency-framework

Django
------

Add packages in :python:`INSTALLED_APPS` in your :bash:`settings.py`.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',

        'cc_framework.blockchain',
        'cc_framework.rest',  # if you need the REST API
    ]

If you specified :python:`cc_framework.rest` application update your
:bash:`urls.py`.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^cc_framework/', include('cc_framework.rest.urls')),
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

:bash:`django-cryptocurrency-framework` interact with blockchains through
cryptocurrency nodes so you should install them and allow RPC access. You
can see configuration example for each supported node in
`example project <https://github.com/madnesspie/django-cryptocurrency-framework/tree/master/example>`_.

Now only following nodes are being supported by the framework:

- Bitcoin: `bitcoin-core <https://bitcoincore.org/en/download/>`_
