from django.urls import path

from web_parameter_tampering.views import (
    home,
    login,
    logout,
    press,
    press_insecure,
    tickets,
)

urlpatterns = [
    path("", home, name="home"),
    path("tickets", tickets, name="tickets"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("press", press, name="press_secure"),
    path("press/<int:user_pk>", press_insecure, name="press_insecure"),
]
