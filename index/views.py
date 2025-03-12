from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *


def index(request):
    return HttpResponse("Hello, world.")


def ver(request):
    v = version.objects.filter(enable=True).order_by("-release_date")
    data = {}
    for i in v:
        data[i.sub] = i.title
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def html(request):
    contents = content.objects.filter(version_id=1).values("id", "title")
    data = list(contents)
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
