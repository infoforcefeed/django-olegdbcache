from django.core.cache.backends.base import BaseCache
from django.utils import six
import requests, msgpack


class OlegDBCache(BaseCache):

    def __init__(self, host, *args, **kwargs):
        self.location = host
        super(OlegDBCache, self).__init__(*args, **kwargs)

    def add(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.get('{}/{}'.format(self.location, key))
        if resp.status_code == 404:
            value = msgpack.packb(data, use_bin_type=True)
            resp = requests.post('{}/{}'.format(self.location, key), data=value)
            return True
        return False

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.get('{}/{}'.format(self.location, key), stream=True)
        if resp.status_code == 404:
            return default
        return msgpack.unpackb(resp.raw.read(), encoding='utf-8')

    def set(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        value = msgpack.packb(value, use_bin_type=True)
        resp = requests.post('{}/{}'.format(self.location, key), data=value)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.delete('{}/{}'.format(self.location, key))

    def get_many(self, keys, version=None):
        many = {}
        for key in keys:
            key = self.make_key(key, version=version)
            self.validate_key(key)
            resp = requests.get('{}/{}'.format(self.location, key), stream=True)
            if resp.status_code != 404:
                many[key] = msgpack.unpackb(resp.raw.read(), encoding='utf-8')
        return many

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.get('{}/{}'.format(self.location, key), stream=True)
        if resp.status_code == 404:
            return False
        return True

    def set_many(self, data, timeout=None, version=None):
        for key, value in data.iteritems():
            key = self.make_key(key, version=version)
            self.validate_key(key)
            self.set(key, value, timeout, version)


    def delete_many(self, keys, version=None):
        for key in keys:
            key = self.make_key(key, version=version)
            self.validate_key(key)
            self.delete(key, value, timeout, version)

    def clear(self):
        raise 'fuck all'
