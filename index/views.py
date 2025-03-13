from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *


def index(request):
    return HttpResponse("Hello, world.")


def menu(request, v=False):
    data = {}

    def parent(obj, d):
        r = to.objects.filter(parent=obj).order_by("-sort")
        for i in r:
            if i.enable:
                if i.link != None:
                    if i.page == "":
                        d["list"][i.link.title] = {
                            "id": i.link.id,
                            "icon": i.icon.url,
                        }
                    else:
                        d["list"][i.link.title] = {
                            "page": i.page,
                            "icon": i.icon.url,
                        }

                else:
                    d["list"][i.title] = {
                        "icon": i.icon.url,
                        "list": {},
                    }
                    parent(i, d["list"][i.title])

    if v:
        game = version.objects.get(sub=v)
        data = {"cover": game.cover.url, "wiki": {}}
        to_list = to.objects.filter(version=game, parent=None).order_by("-sort")
        for t in to_list:
            if t.enable:
                data["wiki"][t.title] = {
                    "list": {},
                }
                parent(t, data["wiki"][t.title])

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
