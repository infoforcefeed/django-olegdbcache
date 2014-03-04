from django.core.cache.backends.base import BaseCache
from django.utils import six
import requests, msgpack, hashlib, pickle


class OlegDBCache(BaseCache):

    def __init__(self, host, *args, **kwargs):
        self.location = host
        super(OlegDBCache, self).__init__(*args, **kwargs)

    def _pack_item(self, value):
        new_value = None
        try:
            new_value = msgpack.packb(value, use_bin_type=True)
        except TypeError:
            new_value = pickle.dumps(value)
        return new_value

    def add(self, key, value, timeout=None, version=None):
        resp = requests.get('{}/{}'.format(self.location, key))
        if resp.status_code == 404:
            self.set(key, value, timeout, version)
            return True
        return False

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.get('{}/{}'.format(self.location, key), stream=True)
        if resp.status_code == 404:
            return default
        return msgpack.unpackb(resp.raw.read(), encoding='utf-8')
        #return pickle.loads(resp.raw.read())

    def set(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        new_value = self._pack_item(value)
        resp = requests.post('{}/{}'.format(self.location, key), data=new_value)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.delete('{}/{}'.format(self.location, key))

    def get_many(self, keys, version=None):
        many = {}
        for key in keys:
            returned = self.get(key, version)
            if returned:
                many[key] = returned
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
            self.set(key, value, timeout, version)

    def delete_many(self, keys, version=None):
        for key in keys:
            self.delete(key, value, timeout, version)

    def clear(self):
        raise 'fuck all'
