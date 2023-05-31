from django.urls import path

from web_parameter_tampering.views import wpt

urlpatterns = [
    path("", wpt, name="test"),
]
