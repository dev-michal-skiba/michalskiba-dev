from django.urls import path

from sql_injection.views import home

urlpatterns = [
    path("", home, name="home"),
]
