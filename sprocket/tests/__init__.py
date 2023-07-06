from django.test import Client
import json


def post_api(url: str, payload: dict = {}, token="", headers: dict = {}):
    client = Client()
    headers["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client.post(url, json.dumps(payload), "application/json", **headers)


def get_api(url: str, payload: dict = {}, token="", headers: dict = {}):
    client = Client()
    headers["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client.get(url, payload, content_type="application/json", **headers)


def delete_api(url: str, payload: dict = {}, token="", headers: dict = {}):
    client = Client()
    headers["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client.delete(url, payload, content_type="application/json", **headers)
