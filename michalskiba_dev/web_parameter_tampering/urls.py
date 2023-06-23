from django.urls import path

from web_parameter_tampering.views import home, press, tickets

urlpatterns = [
    path("", home, name="home"),
    path("tickets", tickets, name="tickets"),
    path("press", press, name="press_secure"),
]
