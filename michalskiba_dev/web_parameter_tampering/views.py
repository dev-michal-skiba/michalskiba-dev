from django.http import HttpRequest, HttpResponse


def wpt(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Web Parameter Tampering Demo - WIP")
