import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-cryptocurrency-framework',
    version='0.1.2',
    packages=find_packages(exclude=['tests*']),
    install_requires=['Django>=2.2.3', 'requests>=2.0.0'],
    extras_require={
        "dev": ['pylint==2.3.1', 'pylint-django==2.0.10']
    },
    include_package_data=True,
    license='GNU Lesser General Public License v3 or later (LGPLv3+)',
    description='A Django app for receiving payments in cryptocurrencies.',
    long_description=README,
    long_description_content_type='text/markdown',
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
