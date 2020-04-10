.. role:: bash(code)
   :language: bash

===========================================
Welcome to django-obm!
===========================================

|travis| |pypi-version| |readthedocs|

.. |travis| image:: https://travis-ci.org/madnesspie/django-obm.svg?branch=master
    :target: https://travis-ci.org/madnesspie/django-obm
    :alt: Travis CI

.. |pypi-version| image:: https://badge.fury.io/py/django-obm.svg
    :target: https://badge.fury.io/py/django-obm
    :alt: PyPI

.. |readthedocs| image:: https://readthedocs.org/projects/django-obm/badge/?version=latest
    :target: https://django-obm.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Rationale
=========
There are a lot of projects that need a cryptocurrency payment system under
the hood for transactions sending/receiving, unique addresses creation, fee
estimating and other blockchain interactions. Each of them have to implement
their own service for that propose due to lack of opensource product, that
could satisfy their needs. This project aims to provide such functionality and
facilitate the implementation of such a microservice.

Resources
=========

- Documentation: https://django-obm.readthedocs.io

Installation
============

See `Installation <https://django-obm.readthedocs.io/en/latest/installation.html>`_ for complete instructions.

.. code-block:: bash

    pip install django-obm

Requirements
============
- Python 3.8 or higher.
- `bitcoin-core <https://bitcoincore.org/en/download/>`_ node

Features
========

- BTC (bitcoin-core) support
- sending/receiving transactions and confirmation
- unique addresses creation
- fee estimating
- REST API for actions above

Future features
---------------

- support of: ETH, ETC, DASH, BCHABC, BCHSV, LTC, ZEC, XEM, XRP, etc.
- :bash:`django_obm.wallet` app witch help in implementation of multi
  cryptocurrency wallet


Is django-obm production ready?
====================================================
The project is now under active development. Use at your own risk.

Example
=======
You can find the example project in this repo
`example folder <https://github.com/madnesspie/django-obm/tree/master/example>`_.

Contributing
============
See `CONTRIBUTING.md <https://github.com/madnesspie/django-obm/blob/master/CONTRIBUTING.md>`_ for instructions.

Support the developer
=====================

Sponsors
--------
Special thanks for `Swapzilla <https://www.swapzilla.co/>`_ project that
paid me part of the development.

.. figure:: https://raw.githubusercontent.com/madnesspie/django-obm/d285241038bb8d325599e8c4dddb567468daae81/docs/swapzilla.jpeg
  :width: 100%
  :figwidth: image
  :alt: Swapzilla logo

You can also become the sponsor and get priority development of the features
you require. Just `contact me <https://github.com/madnesspie>`_.

Buy me a beer
-------------
.. code-block:: bash

    BTC 179B1vJ8LvAQ2r9ABNhp6kDE2yQZfm1Ng3
