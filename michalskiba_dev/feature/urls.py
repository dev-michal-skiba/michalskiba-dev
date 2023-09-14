from django.urls import path

from feature.views import test_sentry

urlpatterns = [
    path("test-sentry", test_sentry, name="test_sentry"),
]
