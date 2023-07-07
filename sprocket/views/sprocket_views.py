from sprocket.utils.utils import add_field_to_response
from sprocket.views import PaginatedView, BaseView
from sprocket.models import Sprocket, SprocketProduction


class GetSprocketProduction(PaginatedView):
    method = "GET"
    allowed_order_filters = [
        "id",
        "sprocket_id",
        "sprocket__teeth",
        "sprocket__teeth__lt",
        "sprocket__teeth__gt",
        "sprocket__pitch_diameter",
        "sprocket__pitch_diameter__lt",
        "sprocket__pitch_diameter__gt",
        "sprocket__outside_diameter",
        "sprocket__outside_diameter__lt",
        "sprocket__outside_diameter__gt",
        "sprocket__pitch",
        "sprocket__pitch__lt",
        "sprocket__pitch__gt",
        "factory_id",
        "factory__name",
        "sprocket_goal",
        "sprocket_goal__lt",
        "sprocket_goal__gt",
        "sprocket_actual",
        "sprocket_actual__lt",
        "sprocket_actual__gt",
        "date_produced",
        "date_produced__lt",
        "date_produced__gt",
    ]
    schema_values = [
        "sprocket_id",
        "sprocket__teeth",
        "sprocket__pitch_diameter",
        "sprocket__outside_diameter",
        "sprocket__pitch",
        "factory_id",
        "factory__name",
        "sprocket_goal",
        "sprocket_actual",
        "date_produced",
    ]
    model = SprocketProduction


class GetSprocket(BaseView):
    method = "GET"
    model = Sprocket
    required_fields = ["id"]


class PostSprocket(BaseView):
    method = "POST"
    model = Sprocket
    required_fields = ["teeth", "pitch_diameter", "outside_diameter", "pitch"]


class PutSprocket(BaseView):
    method = "PUT"
    model = Sprocket
    required_fields = ["id", "teeth", "pitch_diameter", "outside_diameter", "pitch"]
