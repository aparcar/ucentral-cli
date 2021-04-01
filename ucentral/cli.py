from jsonschema import validate, ValidationError
from pathlib import Path
import json
import magicattr as ma
from ast import literal_eval

from ucentral.util import Config


schema = json.load(open("ucentral.schema.json"))


def add(config, string):
    tmp_config = Config()
    tmp_config.update(config)

    if not ma.get(config, string):
        ma.set(config, string, [])

    obj, name, _ = ma.lookup(config, string)
    obj[name].append(Config())

    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return

    config.update(tmp_config)
    print(f"{string}[{len(obj[name]) - 1}]")


def add_list(config, string):
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
    config.update(tmp_config)


def del_list(config, string):
    tmp_config = Config()
    tmp_config.update(config)

    path, value = string.split("=", maxsplit=1)

    if not ma.get(tmp_config, path):
        ma.set(tmp_config, path, [])

    obj, name, _ = ma.lookup(tmp_config, path)
    obj[name].remove(literal_eval(value.strip()))

    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return
    config.update(tmp_config)


def get(config, string):
    obj, name, _ = ma.lookup(config, string)
    print(obj[name])


def set(config, string):
    tmp_config = Config()
    tmp_config.update(config)
    path, value = string.split("=", maxsplit=1)

    ma.set(tmp_config, path.strip(), literal_eval(value.strip()))
    try:
        validate(instance=tmp_config, schema=schema)
    except ValidationError as e:
        print(e)
        return
    config.update(tmp_config)


def usage():
    print(
        """Usage:
  print                 Show current configuration
  get <path>            Show value stored at path
  import <filename>     Import a valid JSON configuration
  commit <filename>     Save configuration to <filename>
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


def parse_cmd(config, cmd):
    if cmd == "print":
        print(json.dumps(config, sort_keys=True, indent=4))

    elif cmd.startswith("import "):
        filename = cmd.split(maxsplit=1)[1]
        tmp_config = json.load(open(filename))
        try:
            validate(instance=tmp_config, schema=schema)
        except ValidationError as e:
            print(e)
            return
        config = tmp_config.copy()

    elif cmd.startswith("commit "):
        filename = cmd.split(maxsplit=1)[1]
        json.dump(config, open(filename, "w"), sort_keys=True, indent=True)
        print(f"Config written to {filename}")

    elif cmd == "help":
        usage()

    elif cmd.startswith("set "):
        set(config, cmd.split(maxsplit=1)[-1])

    elif cmd.startswith("add "):
        add(config, cmd.split(maxsplit=1)[-1])

    elif cmd.startswith("add_list "):
        add_list(config, cmd.split(maxsplit=1)[-1])

    elif cmd.startswith("get "):
        get(config, cmd.split(maxsplit=1)[-1])

    elif cmd.startswith("del_list "):
        del_list(config, cmd.split(maxsplit=1)[-1])

    else:
        usage()


if __name__ == "__main__":
    config = Config()
    while True:
        print(config)
        cmd = input(">> ")
        try:
            parse_cmd(config, cmd)
        except Exception as e:
            # TODO: dirty
            print(e)
