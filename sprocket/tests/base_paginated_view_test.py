import pytest
from django.test import Client
from django.core.management import call_command
from django.urls import reverse
import json

from sprocket.models import Factory, Sprocket


def test_get_api_status():
    """
    Test to verify the API status.
    """
    url = reverse("get_api_status")
    response = Client().get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_sprocket_production_list(db):
    """
    Test to get the list of sprocket production.
    """
    call_command("build_factory_data")
    url = reverse("get_sprocket_production")
    response = Client().get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data["data"]) == 10
    assert data["total_pages"] == 6
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["success"] == True


@pytest.mark.django_db
def test_get_sprocket_production_pagination(db):
    """
    Test to get the paginated list of sprocket production.
    """
    call_command("build_factory_data")
    url = reverse("get_sprocket_production")
    response = Client().get(
        url, {"page": 1, "size": 2}, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["total_pages"] == 30
    assert int(data["page"]) == 1
    assert int(data["size"]) == 2
    assert data["success"] == True


@pytest.mark.django_db
def test_get_sprocket_production_filtered_by_factory(db):
    """
    Test to get the list of sprocket production filtered by factory.
    """
    call_command("build_factory_data")
    url = reverse("get_sprocket_production")
    factory = Factory.objects.first()
    response = Client().get(
        url, {"filter": f"factory_id:{factory.id}"}, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 10
    assert data["total_pages"] == 2
    assert int(data["page"]) == 1
    assert int(data["size"]) == 10
    assert data["success"] == True


@pytest.mark.django_db
def test_get_factory(db):
    """
    Test to get a single factory.
    """
    call_command("build_factory_data")
    factory = Factory.objects.first()
    url = reverse("get_factory", args=[factory.id])
    response = Client().get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data["data"].keys()) == 5
    assert data["success"] == True


@pytest.mark.django_db
def test_get_single_sprocket(db):
    """
    Test to get a single sprocket.
    """
    call_command("build_factory_data")
    sprocket = Sprocket.objects.first()
    url = reverse("get_sprocket", args=[sprocket.id])
    response = Client().get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data["data"].keys()) == 6
    assert data["success"] == True


@pytest.mark.django_db
def test_create_sprocket(db):
    """
    Test to create a new sprocket.
    """
    url = reverse("new_sprocket")
    payload = {
        "teeth": 10,
        "pitch_diameter": 15.5,
        "outside_diameter": 20.2,
        "pitch": 5,
    }
    response = Client().post(url, json.dumps(payload), "application/json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["teeth"] == payload["teeth"]
    assert data["pitch_diameter"] == payload["pitch_diameter"]
    assert data["outside_diameter"] == payload["outside_diameter"]
    assert data["pitch"] == payload["pitch"]


@pytest.mark.parametrize(
    "payload",
    [
        {
            "teeth": 10,
            "pitch_diameter": 15.5,
            "outside_diameter": 20.2,
            "pitch": "asfasf",
        },
        {
            "teeth": 10,
            "pitch_diameter": 15.5,
            "outside_diameter": 20.2,
            "pitch": 5,
            "otherparam": 12,
        },
        {
            "pitch_diameter": 15.5,
            "outside_diameter": 20.2,
            "pitch": 5,
        },
    ],
)
def test_create_wrong_payload_sprocket(payload):
    """
    Test to create a sprocket with wrong payload.
    """
    url = reverse("new_sprocket")
    response = Client().post(url, json.dumps(payload), "application/json")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] == False


@pytest.mark.django_db
def test_update_sprocket(db):
    """
    Test to update a sprocket.
    """
    call_command("build_factory_data")
    sprocket = Sprocket.objects.first()
    url = reverse("update_sprocket", args=[sprocket.id])
    payload = {
        "teeth": 12,
        "pitch_diameter": 16.8,
        "outside_diameter": 21.7,
        "pitch": 6,
    }
    response = Client().put(url, json.dumps(payload), "application/json")
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["teeth"] == payload["teeth"]
    assert data["pitch_diameter"] == payload["pitch_diameter"]
    assert data["outside_diameter"] == payload["outside_diameter"]
    assert data["pitch"] == payload["pitch"]
