from jsonschema import ValidationError

from ucentral.ucentral import Ucentral


def test_validation_bad():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    assert type(uc.set("uuid", "abc")) == ValidationError


def test_merge_good():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    uc.set("foo.bar", 13)
    assert uc.config["foo.bar"] == 13
    uc.merge({"foo": {"baz": 37}})
    assert uc.config["foo.bar"] == 13
    assert uc.config["foo.baz"] == 37


def test_merge_bad():
    uc = Ucentral()
    uc.schema_load("./tests/ucentral.schema.json")
    assert type(uc.merge({"uuid": "abc"})) == ValidationError


def test_bad_del_list():
    uc = Ucentral()
    uc.set("tests", 1)
    assert uc.del_list("tests", 1) == "tests is not a list"
