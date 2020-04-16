import setuptools

import django_obm

EXTRAS_REQUIRE = {
    "tests": ["pytest", "pytest-django", "python-dotenv", "pytest-xdist"],
    "lint": ["pylint", "pylint-django", "mypy"],
    "docs": ["sphinx>=2.4,<3", "sphinx-rtd-theme"],
    "dev": ["tox", "rope"],
}
EXTRAS_REQUIRE["dev"] += (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + EXTRAS_REQUIRE["docs"]
)


def read(file_name):
    with open(file_name) as f:
        content = f.read()
    return content


setuptools.setup(
    name="django-obm",
    version=django_obm.__version__,
    packages=setuptools.find_packages(exclude=["tests*", "example*"]),
    install_requires=[
        "obm<0.1.0",
        "Django>=2.2,<4",
        "djangorestframework>=3,<4",
    ],
    extras_require=EXTRAS_REQUIRE,
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    description=(
        "Django app that provide REST API and ORM-integrated interface for "
        "interaction with blockchains.Django app that provide REST API and "
        "ORM-integrated interface for interaction with blockchains."
    ),
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
