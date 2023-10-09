from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from demo.decorators import version
from sql_injection.utils import get_parcel_stores_from_search_phrase


@version
def home(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    is_secure_version_on: bool = kwargs["is_secure_version_on"]
    address_search_phrase = request.GET.get("address-search-phrase", "")
    parcel_stores = get_parcel_stores_from_search_phrase(
        address_search_phrase, is_secure_version_on
    )
    return render(request, "sql_injection/home.html", {"parcel_stores": parcel_stores})
