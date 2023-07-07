from django.urls import path

from sprocket.views import ApiStatusView
from sprocket.views.sprocket_views import (
    GetSprocketProduction,
    GetSprocket,
    PostSprocket,
    PutSprocket,
)
from sprocket.views.factory_views import GetFactory

urlpatterns = [
    path("status/", ApiStatusView.as_view(), name="get_api_status"),
    path(
        "factory/sprockets",
        GetSprocketProduction.as_view(),
        name="get_sprocket_production",
    ),
    path("factory/<int:id>", GetFactory.as_view(), name="get_factory"),
    path("sprocket/<int:id>", GetSprocket.as_view(), name="get_sprocket"),
    path("sprocket/create", PostSprocket.as_view(), name="new_sprocket"),
    path("sprocket/update", PutSprocket.as_view(), name="update_sprocket"),
]
