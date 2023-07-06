from django.urls import path

from sprocket.views import ApiStatusView
urlpatterns = [
    path("status/", ApiStatusView.as_view(), name="get_api_status"),
]
