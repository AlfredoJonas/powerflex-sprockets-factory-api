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


# The `BaseView` class is a base class for handling HTTP requests and processing payloads in a Django
# view.
class BaseView(View):
    method = "POST"
    required_fields = []
    model = None

    def proccess_payload_post_put(self, request, **kwargs):
        """
        The function processes the payload of a POST or PUT request by decoding the body, loading it as
        JSON, merging it with additional keyword arguments, and then validating the resulting
        parameters.
        
        :param request: The `request` parameter is an object that represents the HTTP request being
        made. It contains information such as the request method (e.g., GET, POST, PUT), headers, and
        body of the request
        :return: the `parameters` variable.
        """
        body_unicode = getattr(request, "body", None).decode("utf-8")
        body = json.loads(body_unicode) if body_unicode else {}
        parameters = {**body, **kwargs}
        self.validate(request, parameters)
        return parameters

    def proccess_payload_get_delete(self, request, **kwargs):
        """
        The function processes a payload by merging the request's GET parameters with additional keyword
        arguments and then validates the resulting parameters.
        
        :param request: The `request` parameter is an object that represents the HTTP request made to
        the server. It contains information such as the request method (GET, POST, etc.), headers, query
        parameters, and the request body
        :return: the "parameters" variable.
        """
        body = request.GET.dict()
        parameters = {**body, **kwargs}
        self.validate(request, parameters)
        return parameters

    def proccess_post_put(self, request, save_update_record, **kwargs):
        """
        The function processes a POST or PUT request, validates the data, saves the record, and returns
        a JSON response.
        
        :param request: The `request` parameter is an object that represents the HTTP request made to
        the server. It contains information such as the request method (GET, POST, PUT, etc.), headers,
        query parameters, and the request body
        :param save_update_record: The `save_update_record` parameter is a function that is responsible
        for saving or updating a record based on the provided parameters. It takes the `parameters` as
        input and should return the saved or updated record
        :return: The code is returning the response object.
        """
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
        """
        The function processes a GET or DELETE request by extracting parameters, making a request, and
        returning a JSON response.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (GET, DELETE, etc.), headers, and
        query parameters
        :param get_delete_record: The `get_delete_record` parameter is a function that takes in the
        `parameters` as an argument and returns the record that needs to be deleted
        :return: the response object after processing the request and adding success to it.
        """
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
        """
        The function validates a payload dictionary by checking for missing or extra fields.
        
        :param payload: The `payload` parameter is a dictionary that contains the data that needs to be
        validated
        :type payload: dict
        """
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
        """
        The function validates the request method and payload against the required fields.
        
        :param request: The `request` parameter is an object that represents the HTTP request being
        made. It typically contains information such as the HTTP method (GET, POST, etc.), headers, and
        other request-specific data
        :param payload: The `payload` parameter is a dictionary that contains the data that needs to be
        validated
        :type payload: dict
        """
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


# The `PaginatedView` class is a base view for paginated API endpoints that allows filtering,
# ordering, and pagination of data.
class PaginatedView(BaseView):
    allowed_order_filters = []
    schema_values = []
    model = None

    def base_query(self, request):
        # Get all objects from the model
        return self.model.objects.all()

    def process_request(self, request, body):
        """
        The function processes a request by filtering, ordering, and paginating data based on the
        provided query parameters.
        
        :param request: The `request` parameter is the HTTP request object that contains information
        about the current request being made to the server. It includes details such as the request
        method (GET, POST, etc.), headers, user authentication, and other metadata
        :param body: The `body` parameter is a dictionary that contains the request body data. It is
        used to retrieve the query parameters for filtering, ordering, pagination, and other options
        :return: a JSON response containing the filtered and ordered data along with pagination
        information. The returned JSON has the following structure:
        """
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
