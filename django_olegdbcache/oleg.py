import requests


class OlegDBCache(BaseCache):

    def __init__(self, host, *args, **kwargs):
        self.location = host

    def add(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = request.get('{}/{}'.format(self.location, key))
        if resp.status_code == 404:
            resp = request.post('{}/{}'.format(self.location, key), data=value)
            return True
        return False

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = requests.get('{}/{}'.format(self.location, key), stream=True)
        if resp.status_code == 404:
            return default
        return resp.raw.read()

    def set(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = request.post('{}/{}'.format(self.location, key), data=value)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        resp = request.delete('{}/{}'.format(self.location, key))

    def get_many(self, keys, version=None):
        many = {}
        for key in keys:
            key = self.make_key(key, version=version)
            self.validate_key(key)
            resp = requests.get('{}/{}'.format(self.location, key), stream=True)
            if resp.status_code != 404:
                many[key] = resp.raw.read()
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
