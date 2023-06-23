from django.urls import path

from web_parameter_tampering.views import home

urlpatterns = [
    path("", home, name="home"),
]
