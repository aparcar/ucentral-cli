import json
from ast import literal_eval
from sys import argv

import magicattr as ma
from jsonschema import ValidationError, validate

from ucentral.ucentral import Ucentral
from ucentral.util import Config

usage = """Usage:
  show                      Show current configuration
  get <path>                Show value stored at path
  set <path>=<value>        Set value, e.g. log.log_size=64
  add <path>                Add object to list at <path>
  load <filename>           Import a valid JSON configuration
  write <filename>          Save configuration to <filename>
  add_list <path>=<value>   Add empty object to list
  del_list <path>=<value>   Add value to list

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


def parse_cmd(uc, cmd):
    operation, *argument = cmd.split(maxsplit=1)
    if operation == "show":
        uc.show()

    elif operation == "set":
        return uc.set(argument[0])

    elif operation == "add":
        return uc.add(argument[0])

    elif operation == "get":
        return uc.get(argument[0])

    elif operation == "add_list":
        return uc.add_list(argument[0])

    elif operation == "del_list":
        return uc.del_list(argument[0])

    elif operation == "load":
        return uc.load(argument[0])

    elif operation == "write":
        return uc.write(argument[0])

    elif operation == "schema_load":
        return uc.load_schema(argument[0])

    else:
        return usage


def loop():
    uc = Ucentral()
    if len(argv) == 2:
        uc.schema_load(argv[1])
    else:
        uc.schema_load("ucentral.schema.json")

    while True:
        cmd = input(">> ")
        try:
            print(parse_cmd(uc, cmd))
        except Exception as e:
            # TODO: dirty
            print(e)


if __name__ == "__main__":
    loop()
