.. role:: bash(code)
   :language: bash

===========================================
Welcome to django-cryptocurrency-framework!
===========================================

|travis| |pypi-version| |readthedocs|

.. |travis| image:: https://travis-ci.org/madnesspie/django-cryptocurrency-framework.svg?branch=master
    :target: https://travis-ci.org/madnesspie/django-cryptocurrency-framework
    :alt: Travis CI

.. |pypi-version| image:: https://badge.fury.io/py/django-cryptocurrency-framework.svg
    :target: https://badge.fury.io/py/django-cryptocurrency-framework
    :alt: PyPI

.. |readthedocs| image:: https://readthedocs.org/projects/django-cryptocurrency-framework/badge/?version=latest
    :target: https://django-cryptocurrency-framework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Rationale
=========
There are a lot of project that need a cryptocurrency payment system under
the hood for transactions sending/receiving, unique addresses creation, fee
estimating and other blockchain interactions. Each of them have to implement
their own service for that propouse due to lack of opensource product, that
could satisfy their need. This project aims to provide such functionality and
facilitate the implementation of such a microservice

Resources
=========

- Documentation: https://django-cryptocurrency-framework.readthedocs.io

Installation
============

See `Installation <https://django-cryptocurrency-framework.readthedocs.io/en/latest/installation.html>`_ for complete instructions.

.. code-block:: bash

    pip install django-cryptocurrency-framework

Requirements
============
- Python 3.6 or higher.
- `bitcoin-core <https://bitcoincore.org/en/download/>`_ node

Features
========

- BTC (bitcoin-core) support
- transactions sending/receiving and confirmation
- unique addresses creation
- fee estimating
- REST API for actions above

Future features
---------------

- support for: ETH, ETC, DASH, BCHABC, BCHSV, LTC, ZEC, XEM, XRP and so on
- :bash:`cc_framework.wallet` app that help in implementation multi
  cryptocurrency wallet


Is django-cryptocurrency-framework production ready?
====================================================
The project is now under active development. Use at your own risk.

Example
=======
You can find the example project in this repo
`example folder <https://github.com/madnesspie/django-cryptocurrency-framework/tree/master/example>`_.

Contributing
============
See `CONTRIBUTING.md <https://github.com/madnesspie/django-cryptocurrency-framework/blob/master/CONTRIBUTING.md>`_ for instructions.

Support the developer
=====================

Sponsors
--------
Special thanks for `Swapzilla <https://www.swapzilla.co/>`_ project that
paid me part of the development.

.. figure:: https://raw.githubusercontent.com/madnesspie/django-cryptocurrency-framework/d285241038bb8d325599e8c4dddb567468daae81/docs/swapzilla.jpeg
  :width: 100%
  :figwidth: image
  :alt: Swapzilla logo

You can also become the sponsor and get priority development of the features
you need. Just `contact me <https://github.com/madnesspie>`_.

Buy me a beer
-------------
.. code-block:: bash

    BTC 179B1vJ8LvAQ2r9ABNhp6kDE2yQZfm1Ng3
