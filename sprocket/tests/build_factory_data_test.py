import pytest
from django.core.management import call_command
from sprocket.models import Sprocket, Factory, SprocketProduction
from django.core.management.base import CommandError


def get_json_data():
    from sprocket.utils.utils import read_json_file

    factory_json = read_json_file("sprocket/fixtures/seed_factory_data.json")
    sprockets_json = read_json_file("sprocket/fixtures/seed_sprocket_types.json")
    return factory_json, sprockets_json


# Tests that sprockets and factories are created successfully
@pytest.mark.django_db
def test_successful_creation(db):
    call_command("build_factory_data")
    assert Sprocket.objects.count() == 3
    assert Factory.objects.count() == 3
    assert SprocketProduction.objects.count() == 60


# Tests that sprocket and factory data is not created if sprocket data is missing required fields
@pytest.mark.django_db
def test_missing_sprocket_fields(db, monkeypatch):
    factory_json, sprockets_json = get_json_data()
    sprockets_json["sprockets"][0].pop("teeth")
    monkeypatch.setattr(
        "sprocket.utils.utils.read_json_file",
        lambda url: sprockets_json if "seed_sprocket_types" in url else factory_json,
    )
    with pytest.raises(Exception):
        call_command("build_factory_data")
    assert Sprocket.objects.count() == 0
    assert Factory.objects.count() == 0
    assert SprocketProduction.objects.count() == 0


# Tests that sprocket and factory data is not created if factory data is missing required fields
@pytest.mark.django_db
def test_missing_factory_fields(db, monkeypatch):
    factory_json, sprockets_json = get_json_data()
    factory_json["factories"][0]["factory"].pop("chart_data")
    monkeypatch.setattr(
        "sprocket.utils.utils.read_json_file",
        lambda url: sprockets_json if "seed_sprocket_types" in url else factory_json,
    )
    with pytest.raises(Exception):
        call_command("build_factory_data")
    assert Sprocket.objects.count() == 0
    assert Factory.objects.count() == 0
    assert SprocketProduction.objects.count() == 0
