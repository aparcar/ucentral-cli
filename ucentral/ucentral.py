import json
from ast import literal_eval

import magicattr as ma
from jsonschema import ValidationError, validate

from ucentral.util import Config, merge


class Ucentral:
    def __init__(self):
        self.config = Config()
        self.schema = {}
        self.last_load_path = None
        self.last_schema_path = None
        self.last_write_path = None

    def add(self, string):
        tmp_config = Config()
        tmp_config.update(self.config)

        if not ma.get(self.config, string):
            ma.set(self.config, string, [])

        obj, name, _ = ma.lookup(self.config, string)
        obj[name].append(Config())

        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e

        self.config.update(tmp_config)
        return f"{string}[{len(obj[name]) - 1}]"

    def add_list(self, string):
        tmp_config = Config()
        tmp_config.update(self.config)

        path, value = string.split("=", maxsplit=1)

        if not ma.get(tmp_config, path):
            ma.set(tmp_config, path, [])

        obj, name, _ = ma.lookup(tmp_config, path)
        obj[name].append(literal_eval(value.strip()))

        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e
        self.config.update(tmp_config)

    def del_list(self, string):
        tmp_config = Config()
        tmp_config.update(self.config)

        path, value = string.split("=", maxsplit=1)

        if not ma.get(tmp_config, path):
            ma.set(tmp_config, path, [])

        obj, name, _ = ma.lookup(tmp_config, path)
        obj[name].remove(literal_eval(value.strip()))

        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e
        self.config.update(tmp_config)

    def get(self, string):
        obj, name, _ = ma.lookup(self.config, string)
        return obj[name]

    def set(self, string):
        tmp_config = Config()
        tmp_config.update(self.config)
        path, value = string.split("=", maxsplit=1)

        ma.set(tmp_config, path.strip(), literal_eval(value.strip()))

        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e

        self.config.update(tmp_config)
        return True

    def show(self):
        return json.dumps(self.config, sort_keys=True, indent=4)

    def load(self, filename: str):
        if not filename:
            filename = self.last_load_path

        tmp_config = json.load(open(filename))
        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e

        self.config.update(tmp_config)

    def schema_load(self, filename: str):
        if not filename:
            filename = self.last_schema_path
        self.schema = json.load(open(filename))

        self.last_schema_path = filename
        return True

    def write(self, filename: str = None):
        if not filename:
            filename = self.last_write_path

        json.dump(self.config, open(filename, "w"), sort_keys=True, indent=4)

        self.last_write_path = filename

        return f"Config written to {filename}"

    def merge(self, obj):
        tmp_config = Config()
        tmp_config.update(self.config)

        merge(obj, tmp_config)
        try:
            validate(instance=tmp_config, schema=self.schema)
        except ValidationError as e:
            return e

        self.config.update(tmp_config)
