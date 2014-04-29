from setuptools import setup

setup(
    author="Kyle Terry and Quinlan Pfiffer",
    url="https://github.com/infoforcefeed/django-olegdbcache",
    name="django-olegdbcache",
    description="ERM?",
    version="0.1.0a",
    license="BSD?",
    keywords="olegdb django",
    packages=["django_olegdbcache",],
    zip_safe=True,
    install_requires = [
        "django",
        "msgpack-python",
        "requests",
        "olegdb-python",
    ]
)
