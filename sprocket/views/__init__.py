from typing import Any
from django.views import View
from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from sprocket.utils.exceptions import BadRequest, MethodNotAllowed, NotFound
import json
from sprocket.utils.model_queries import (
    query_filter_to_paginated_api_view,
    query_order_to_paginated_api_view,
)
from sprocket.utils.utils import add_field_to_response, check_keys_on_dict


class BaseView(View):
    method = "POST"
    required_fields = []
    model = None

    def proccess_payload_post_put(self, request, **kwargs):
        body_unicode = getattr(request, "body", None).decode("utf-8")
        body = json.loads(body_unicode) if body_unicode else {}
        parameters = {**body, **kwargs}
        self.validate(request, parameters)
        return parameters

    def proccess_payload_get_delete(self, request, **kwargs):
        body = request.GET.dict()
        parameters = {**body, **kwargs}
        self.validate(request, parameters)
        return parameters

    def proccess_post_put(self, request, save_update_record, **kwargs):
        try:
            parameters = self.proccess_payload_post_put(request, **kwargs)
            response = self.process_request(request, parameters)
        except NotImplementedError as e:
            try:
                record = save_update_record(parameters)
                record.full_clean()
                record.save()
                response = JsonResponse(
                    {
                        "data": model_to_dict(record),
                    }
                )
                return response
            except ObjectDoesNotExist:
                raise NotFound
            except ValidationError as e:
                raise BadRequest(f"Invalid data provided: {str(e)}")
        return self.add_success(response)

    def proccess_get_delete(self, request, get_delete_record, **kwargs):
        parameters = self.proccess_payload_get_delete(request, **kwargs)
        try:
            response = self.process_request(request, parameters)
        except NotImplementedError:
            record = get_delete_record(parameters)
            response = JsonResponse(
                {
                    "data": model_to_dict(record),
                }
            )
        return self.add_success(response)

    @staticmethod
    def add_success(response, key="success", status=True):
        return add_field_to_response(response, key, status)

    def validate_payload(self, payload: dict):
        message = None
        missing_fields = check_keys_on_dict(self.required_fields, payload)
        more_fields = len(list(payload.keys())) > len(self.required_fields)
        if missing_fields:
            message = "You miss one or more required fields on the payload: "
        elif more_fields:
            message = "You have more fields on the payload than the ones required: "
        if message:
            raise BadRequest(message + ",".join(self.required_fields))

    def validate(self, request, payload: dict):
        if request.method != self.method:
            raise MethodNotAllowed
        elif len(self.required_fields) > 0:
            self.validate_payload(payload)

    def post(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        def save_record(parameters):
            record = self.model(**parameters)
            return record

        return self.proccess_post_put(request, save_record, **kwargs)

    def put(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        def update_record(parameters):
            record = self.model.objects.get(id=parameters.get("id"))
            for key, value in parameters.items():
                setattr(record, key, value)
            return record

        return self.proccess_post_put(request, update_record, **kwargs)

    def get(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        get_record = lambda p: self.model.objects.get(id=p.get("id"))
        return self.proccess_get_delete(request, get_record, **kwargs)

    def delete(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        def delete_record(parameters):
            record = self.model.objects.get(id=parameters.get("id"))
            record.deleted = True
            record.save()

        return self.proccess_get_delete(request, delete_record, **kwargs)

    def process_request(self, request: WSGIRequestHandler, body: dict):
        raise NotImplementedError


class PaginatedView(BaseView):
    allowed_order_filters = []
    schema_values = []
    model = None

    def base_query(self, request):
        # Get all objects from the model
        return self.model.objects.all()

    def process_request(self, request, body):
        # Get query parameters for filtering and ordering
        filter_param = body.get("filter", "")
        order_param = body.get("order", "")
        ordering_conditions = []

        queryset = self.base_query(request)

        # Check if model has deleted field and then use it to filter deleted data
        if hasattr(self.model, "deleted"):
            queryset = queryset.filter(deleted=0)

        # Apply filtering if filter_param is provided
        if filter_param:
            # Split the filters into individual filter conditions
            filter_conditions = filter_param.split(",")
            queryset = query_filter_to_paginated_api_view(
                self.allowed_order_filters, filter_conditions, queryset
            )

        # Apply ordering if order_param is provided
        if order_param:
            # Split the ordering into individual ordering conditions
            ordering_conditions = order_param.split(",")
        elif hasattr(self.model, "date_created"):
            # Check if model has date_created field and then use it to order by default to keep consistency data
            ordering_conditions = ["-date_created"]

        if len(ordering_conditions) > 0:
            queryset = query_order_to_paginated_api_view(
                self.allowed_order_filters, ordering_conditions, queryset
            )

        # Pagination
        page_number = body.get("page", 1)
        size = body.get("size", 10)
        paginator = Paginator(queryset, size)
        try:
            page_obj = paginator.page(page_number)
            data = list(
                page_obj.object_list.values(
                    *(self.schema_values if self.schema_values else [])
                )
            )
        except Exception:
            # Handle invalid page number gracefully
            data = []

        pagination_data = {
            "total_pages": paginator.num_pages,
            "page": 1,
            "size": 10,
            **body,
        }
        return JsonResponse({"data": data, **pagination_data})


class ApiStatusView(View):
    def get(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        data = {"status": "OK"}
        return JsonResponse(data)
