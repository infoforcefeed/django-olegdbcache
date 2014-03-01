# OlegDB Cache Backend for Django

Quick setup SO SPEED
--------------------

Add to your settings file:

````
CACHES = {
    "default": {
        "BACKEND": "django_olegdbcache.oleg.OlegDBCache",
        "LOCATION": "http://localhost:8080"
    }
}
````
