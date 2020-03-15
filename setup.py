import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django-cryptocurrency-framework',
    version='0.1.6',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=2.2,<4',
        'requests>=2,<3',
        'djangorestframework>=3,<4',
    ],
    extras_require={
        'dev': [
            'sphinx',
            'pytest',
            'pytest-django',
            'pylint',
            'pylint-django',
            'mypy',
            'rope',
        ],
    },
    license='GNU Lesser General Public License v3 or later (LGPLv3+)',
    description='A Django app for receiving payments in cryptocurrencies.',
    long_description=README,
    url='https://github.com/HelloCreepy/django-cryptocurrency-framework',
    author='Alexander Polishchuk',
    author_email='apolishchuk52@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
