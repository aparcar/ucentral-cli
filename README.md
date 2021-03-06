# ucentral cli

Create and modify valid [ucentral-schema][1] schemata.

[1]: https://github.com/blogic/ucentral-schema

## Installation

    pip install ucentral

The latest [ucentral.schema.json][2] is required in the main folder.

[2]: https://raw.githubusercontent.com/blogic/ucentral-schema/main/ucentral.schema.json

## Usage

Run CLI via `ucentral`

Supported commands:

    add          Add an anonymous obejct to the given configuration.
    add-list     Add the given value to a list option.
    base64       Set <path> to base64 encoded content <filename>
    del-list     Delete element <value> from list at <path>
    file         Set <path> to content of <filename>
    get          Return value from <path>
    load         Load configuration from JSON at <filename>
    schema-load  Load JSON schema from <filename>
    set          Set <path> to <value>
    show         Show current configuration
    write        Store configuration as JSON at <filename>

Type `help <command>` to see usage.

## Examples

    >> set uuid 123
    >> set network.0.cfg.dhcp.leasetime 12h
    >> set network.0.cfg.leases.0.hostname Apollo
    >> add_list ntp.server ntp.example.org
    >> add_list ntp.server ntp.example.com
    >> show

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
