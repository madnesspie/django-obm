import setuptools

import django_obm


def read(file_name):
    with open(file_name) as f:
        content = f.read()
    return content


setuptools.setup(
    name="django-obm",
    version=django_obm.__version__,
    packages=setuptools.find_packages(exclude=["tests*", "example*"]),
    install_requires=[
        "obm<1.0.0",
        "Django>=2.2,<4",
        "requests>=2,<3",
        "djangorestframework>=3,<4",
    ],
    extras_require={
        "dev": [
            "sphinx>=2.4,<3",
            "sphinx-rtd-theme",
            "python-dotenv",
            "pytest",
            "pytest-django",
            "pylint",
            "pylint-django",
            "mypy",
            "rope",
        ],
    },
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    description="A Django app for receiving payments in cryptocurrencies.",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    url="https://github.com/HelloCreepy/django-obm",
    author="Alexander Polishchuk",
    author_email="apolishchuk52@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
