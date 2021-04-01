from ucentral.cli import parse_cmd
from ucentral.util import Config
from ucentral.ucentral import Ucentral


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


def test_merge():
    uc = Ucentral()
    uc.set("foo.bar=13")
    assert uc.config.foo.bar == 13
    uc.merge({"foo": {"baz": 37}})
    assert uc.config.foo.bar == 13
    assert uc.config.foo.baz == 37
