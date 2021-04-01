class Config(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            self[key] = value = Config()
            return value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
