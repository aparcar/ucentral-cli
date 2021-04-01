# ucentral cli

Create and modify valid [ucentral-schema][1] schemata.

[1]: https://github.com/blogic/ucentral-schema

## Installation

    pip install -e .

The latest [ucentral.schema.json][2] is required in the main folder.

[2]: https://raw.githubusercontent.com/blogic/ucentral-schema/main/ucentral.schema.json

## Usage

Run CLI via `ucentral`

    show                      Show current configuration
    get <path>                Show value stored at path
    set <path>=<value>        Set value, e.g. log.log_size=64
    add <path>                Add object to list at <path>
    load <filename>           Import a valid JSON configuration
    write <filename>          Save configuration to <filename>
    add_list <path>=<value>   Add empty object to list
    del_list <path>=<value>   Add value to list

## Examples

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
