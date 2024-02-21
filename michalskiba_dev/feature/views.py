from django.http import HttpRequest, HttpResponse

from feature.flags import ENABLE_SENTRY_TESTING_ENDPOINT, is_flag_enabled


def test_sentry(request: HttpRequest) -> HttpResponse:
    if is_flag_enabled(ENABLE_SENTRY_TESTING_ENDPOINT):
        1 / 0
    return HttpResponse("sentry test disabled")
