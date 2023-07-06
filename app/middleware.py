from django.http import JsonResponse


def is_registered(exception):
    try:
        return exception.is_an_error_response
    except AttributeError:
        return False


class RequestExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if is_registered(exception):
            status = exception.status_code
            exception_dict = exception.to_dict()
        else:
            status = 500
            exception_dict = {"developer_message": "Unexpected Error!"}

        if status != 200:
            exception_dict["success"] = False

        return JsonResponse(exception_dict, status=status)
