import json

import pytest
from click.testing import CliRunner
from dotty_dict import dotty
from jsonschema import ValidationError

import ucentral.cli as cli
from ucentral.ucentral import Ucentral


def test_parse_cmd():
    runner = CliRunner()
    runner.invoke(cli.schema_load, ["./tests/ucentral.schema.json"])
    runner.invoke(cli.set, ["uuid", "123"])
    runner.invoke(cli.set, ["network.0.cfg.dhcp.leasetime", "12h"])
    runner.invoke(cli.set, ["network.0.cfg.leases.0.hostname", "Apollo"])
    runner.invoke(cli.add_list, ["ntp.server", "ntp.example.org"])
    runner.invoke(cli.add_list, ["ntp.server", "ntp.example.com"])
    runner.invoke(cli.del_list, ["ntp.server", "ntp.example.com"])
    config = dotty(json.loads(runner.invoke(cli.show).output))
    assert config["uuid"] == 123
    assert config["network.0.cfg.dhcp.leasetime"] == "12h"
    assert config["network.0.cfg.leases.0.hostname"] == "Apollo"
    assert config["ntp.server"] == ["ntp.example.org"]
