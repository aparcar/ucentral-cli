from ucentral.cli import parse_cmd
from ucentral.util import Config

def test_parse_cmd():
    config = Config()
    parse_cmd(config, 'set uuid=123')
    assert config.uuid == 123
    parse_cmd(config, 'add network')
    assert config.network[0] == {}
    parse_cmd(config, 'set network[0].cfg.dhcp.leasetime="12h"')
    assert config.network[0].cfg.dhcp.leasetime == "12h"
    parse_cmd(config, 'add network[0].cfg.leases')
    assert config.network[0].cfg.leases[0] == {}
    parse_cmd(config, 'set network[0].cfg.leases[0].hostname="Apollo"')
    assert config.network[0].cfg.leases[0].hostname == "Apollo"
    parse_cmd(config, 'add_list ntp.server = "ntp.example.org"')
    parse_cmd(config, 'add_list ntp.server = "ntp.example.com"')
    assert config.ntp.server == ["ntp.example.org", "ntp.example.com" ]
