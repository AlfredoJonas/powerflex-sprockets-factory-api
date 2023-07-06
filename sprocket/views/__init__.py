from typing import Any
from django.views import View
from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse


class ApiStatusView(View):
    def get(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        data = {"status": "OK"}
        return JsonResponse(data)
