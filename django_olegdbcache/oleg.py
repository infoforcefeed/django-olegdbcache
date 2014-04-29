from django.core.cache.backends.base import BaseCache
from django.utils import six
from olegdb import OlegDB, DEFAULT_PORT
import requests, msgpack, hashlib, pickle, re


class OlegDBCache(BaseCache):
    def __init__(self, host, *args, **kwargs):
        https_regex = re.compile(r"https?://")
        host = https_regex.sub("", host)

        regex = re.compile(r"\:(?P<port>[0-9]+)\/?")
        host = regex.sub("", host)

        matched = regex.findall(host)
        if not matched:
            port = DEFAULT_PORT
        else:
            port = matched[0]

        self.connection = OlegDB(host, port)
        super(OlegDBCache, self).__init__(*args, **kwargs)

    def add(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.connection.add(key, value, timeout)

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.connection.get(key, default)

    def set(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.connection.set(key, value, timeout)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.connection.delete(key)

    def get_many(self, keys, version=None):
        new_keys = [self.make_key(key, version=version) for key in keys]
        [self.validate_key(key) for key in new_keys]
        return self.connection.get_many(new_keys)

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.connection.has_key(key)

    def set_many(self, data, timeout=None, version=None):
        for key, value in data.iteritems():
            self.set(key, value, timeout, version)

    def delete_many(self, keys, version=None):
        for key in keys:
            self.delete(key, value, timeout, version)

    def clear(self):
        raise 'fuck all'
