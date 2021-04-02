import pytest
from jsonschema import ValidationError

from ucentral.cli import parse_cmd
from ucentral.ucentral import Ucentral
from ucentral.util import Config


def test_parse_cmd():
    uc = Ucentral()
    parse_cmd(uc, "set uuid=123")
    assert uc.config.uuid == 123
    parse_cmd(uc, "add network")
    assert uc.config.network[0] == {}
    parse_cmd(uc, 'set network[0].cfg.dhcp.leasetime="12h"')
    assert uc.config.network[0].cfg.dhcp.leasetime == "12h"
    parse_cmd(uc, "add network[0].cfg.leases")
    assert uc.config.network[0].cfg.leases[0] == {}
    parse_cmd(uc, 'set network[0].cfg.leases[0].hostname="Apollo"')
    assert uc.config.network[0].cfg.leases[0].hostname == "Apollo"
    parse_cmd(uc, 'add_list ntp.server = "ntp.example.org"')
    parse_cmd(uc, 'add_list ntp.server = "ntp.example.com"')
    assert uc.config.ntp.server == ["ntp.example.org", "ntp.example.com"]
    parse_cmd(uc, 'del_list ntp.server = "ntp.example.com"')
    assert uc.config.ntp.server == ["ntp.example.org"]


def test_validation_bad():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    assert type(uc.set('uuid="abc"')) == ValidationError


def test_merge_good():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    uc.set("foo.bar=13")
    assert uc.config.foo.bar == 13
    uc.merge({"foo": {"baz": 37}})
    assert uc.config.foo.bar == 13
    assert uc.config.foo.baz == 37


def test_merge_bad():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    assert type(uc.merge({"uuid": "abc"})) == ValidationError
