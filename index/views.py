from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *


def index(request):
    return HttpResponse("Hello, world.")


def menu(request, v=False):
    data = {}
    if v:
        chapter_list = chapter.objects.filter(version__sub=v).order_by("id")
        for i in chapter_list:
            data[i.name] = [
                list(content.objects.filter(chapter=i).values("id", "title", "icon"))
            ]
    else:
        v = version.objects.filter(enable=True).order_by("-release_date")
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


def html(request, id):
    i = content.objects.get(id=id)
    data = {
        "title": i.title,
        "time": i.lastmodified.strftime("%Y年%m月%d日 %H:%M"),
        "text": i.text.replace("\r\n", ""),
    }
    return JsonResponse(
        data,
        safe=True,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
