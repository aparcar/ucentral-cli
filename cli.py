from jsonschema import validate, ValidationError
from pathlib import Path
import json
import magicattr as ma
from ast import literal_eval


class Config(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            self[key] = value = Config()
            return value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


schema = json.load(open("ucentral.schema.json"))
config = Config()


def add(string):
    global config
    tmp_config = Config()
    tmp_config.update(config)

    if not ma.get(tmp_config, string):
        ma.set(tmp_config, string, [])

    obj, name, _ = ma.lookup(tmp_config, string)
    obj[name].append(Config())

    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return
    config = tmp_config.copy()
    print(f"{string}[{len(obj[name]) - 1}]")


def add_list(string):
    global config
    tmp_config = Config()
    tmp_config.update(config)

    path, value = string.split("=", maxsplit=1)

    if not ma.get(tmp_config, path):
        ma.set(tmp_config, path, [])

    obj, name, _ = ma.lookup(tmp_config, path)
    obj[name].append(literal_eval(value.strip()))

    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return
    config = tmp_config.copy()

def set(string):
    global config
    tmp_config = Config()
    tmp_config.update(config)
    path, value = string.split("=", maxsplit=1)

    ma.set(tmp_config, path.strip(), literal_eval(value.strip()))
    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return
    config = tmp_config.copy()


def usage():
    print(
        """Usage:
  print                 Show current configuration
  write <filename>      Save configuration to <filename>
  set <path>=<value>    Set value, e.g. log.log_size=64
  add <path>            Add object to list at <path>

Examples:
  >> set uuid=123
  >> add network
  network[0]
  >> set network[0].cfg.dhcp.leasetime='12h'
  >> add network[0].cfg.leases
  network[0].cfg.leases[0]
  >> set network[0].cfg.leases[0].hostname=Apollo
  >> add_list ntp.server = "ntp.example.org"
  >> add_list ntp.server = "ntp.example.com"
  >> print

  {
      "network": [
          {
              "cfg": {
                  "dhcp": {
                      "leasetime": "12h"
                  },
                  "leases": [
                      {
                          "hostname": "Apollo"
                      }
                  ]
              }
          }
      ],
      "ntp": {
          "server": [
              "ntp.example.org",
              "ntp.example.com"
          ]
      },
      "uuid": 123
  }
  """
    )


while True:
    cmd = input(">> ")
    if cmd == "print":
        print(json.dumps(config, sort_keys=True, indent=4))

    elif cmd.startswith("write "):
        filename = cmd.split(maxsplit=1)[1]
        json.dump(config, open(filename, "w"), sort_keys=True, indent=True)
        print(f"Config written to {filename}")

    elif cmd == "help":
        usage()

    elif cmd.startswith("set "):
        set(cmd.split(maxsplit=1)[-1])

    elif cmd.startswith("add "):
        add(cmd.split(maxsplit=1)[-1])
    elif cmd.startswith("add_list "):
        add_list(cmd.split(maxsplit=1)[-1])
    else:
        usage()
