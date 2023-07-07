from sprocket.models import Factory
from sprocket.views import BaseView


class GetFactory(BaseView):
    method = "GET"
    model = Factory
    required_fields = ["id"]
