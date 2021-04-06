import json

import pytest
from click.testing import CliRunner
from dotty_dict import dotty
from jsonschema import ValidationError

import ucentral.cli as cli
from ucentral.ucentral import Ucentral
from ucentral import __version__

from tempfile import TemporaryFile
from os import chdir, getcwd


def test_cli_no_schema(tmp_path):
    cwd = getcwd()
    chdir(tmp_path)

    runner = CliRunner()
    result = runner.invoke(cli.cli)

    try:
        assert (
            result.output
            == f"ucentral cli v{__version__}\nNo schema loaded, please run `schema-load <filename>`\n>> \n"
        )
    finally:
        chdir(cwd)

def test_cli_schema(tmp_path):
    cwd = getcwd()
    chdir("./tests/")

    runner = CliRunner()
    result = runner.invoke(cli.cli)

    try:
        assert (
            result.output
            == f"ucentral cli v{__version__}\nLoaded schema `ucentral.schema.json`\n>> \n"
        )
    finally:
        chdir(cwd)


def test_cmds():
    runner = CliRunner()
    runner.invoke(cli.schema_load, ["./tests/ucentral.schema.json"])
    runner.invoke(cli.set, ["uuid", "123"])
    runner.invoke(cli.set, ["network.0.cfg.dhcp.leasetime", "12h"])
    runner.invoke(cli.set, ["network.0.cfg.leases.0.hostname", "Apollo"])
    runner.invoke(cli.add_list, ["ntp.server", "ntp.example.org"])
    runner.invoke(cli.add_list, ["ntp.server", "ntp.example.com"])
    runner.invoke(cli.del_list, ["ntp.server", "ntp.example.com"])
    runner.invoke(cli.file, ["tests.file", "./tests/plain.txt"])
    runner.invoke(cli.base64, ["tests.base64", "./tests/plain.txt"])
    runner.invoke(cli.add, ["tests.add"])
    config = dotty(json.loads(runner.invoke(cli.show).output))
    assert config["uuid"] == 123
    assert config["network.0.cfg.dhcp.leasetime"] == "12h"
    assert config["network.0.cfg.leases.0.hostname"] == "Apollo"
    assert config["ntp.server"] == ["ntp.example.org"]
    assert config["tests.file"] == "Hello World!\n"
    assert config["tests.base64"] == "SGVsbG8gV29ybGQhCg=="
    assert config["tests.add"] == [{}]
    assert runner.invoke(cli.get, ["tests.file"]).output == '"Hello World!\\n"\n'


def test_cli_load():
    runner = CliRunner()
    runner.invoke(cli.load, ["./tests/simple.json"])
    assert runner.invoke(cli.get, ["simple"]).output == "42\n"


def test_cli_write(tmp_path):
    runner = CliRunner()
    runner.invoke(cli.set, ["foo", "bar"])
    runner.invoke(cli.write, [str(tmp_path / "out.json")])
    assert json.loads((tmp_path / "out.json").read_text())["foo"] == "bar"
