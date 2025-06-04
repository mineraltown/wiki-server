from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import *
import re


def index(request):
    return redirect("https://wiki.mineraltown.net/",permanent=True)


def menu(request, v=False):
    data = {}

    def parent(obj, d):
        r = to.objects.filter(parent=obj).order_by("-sort")
        for i in r:
            if i.enable:
                if i.link != None:
                    d["list"][i.link.title] = {
                        "id": i.link.id,
                        "icon": request.build_absolute_uri("/")[:-1] + i.icon.url,
                    }
                else:
                    if i.page != "":
                        d["list"][i.title] = {
                            "page": i.page,
                            "icon": request.build_absolute_uri("/")[:-1] + i.icon.url,
                        }
                    else:
                        d["list"][i.title] = {
                            "icon": request.build_absolute_uri("/")[:-1] + i.icon.url,
                            "list": {},
                        }
                        parent(i, d["list"][i.title])

    if v:
        game = version.objects.get(sub=v)
        data = {
            "cover": request.build_absolute_uri("/")[:-1] + game.cover.url,
            "wiki": {},
        }
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
            data[i.sub] = i.title.lstrip("牧场物语 ")
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
        "text": i.text.replace("\r\n", "")
        .replace(
            'src="/static/', f"src=\"{request.build_absolute_uri('/')[:-1]}/static/"
        )
        .replace(
            'src="/media/', f"src=\"{request.build_absolute_uri('/')[:-1]}/media/"
        ),
    }
    return JsonResponse(
        data,
        safe=True,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def translate_query(request):
    data = {}

    if "key" in request.GET:
        # 转义关键字中的特殊字符（避免正则注入）
        escaped_key = re.escape(request.GET["key"])
        # 构建查询条件
        """
        (^|;) 匹配字符串的 开头 或 分号 ;
        %s 搜索关键词
        (;|$) 匹配字符串的 结尾 或 分号 ;
        """
        query = (
            Q(cn=request.GET["key"])  # 匹配 cn 字段
            | Q(jp=request.GET["key"])  # 匹配 jp 字段
            | Q(other__iregex=r"(^|;)%s(;|$)" % escaped_key)  # 匹配 other 分割后的元素
        )
        # 执行查询
        r = translate.objects.filter(query)
        for i in r:
            data[i.jp] = [i.cn]
            if i.other != "":
                data[i.jp] += i.other.split(";")
    else:
        r = translate.objects.all()
        for i in r:
            data[i.jp] = i.cn

    return JsonResponse(
        data,
        safe=True,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def replacementMap(request):
    data = {}

    r = translate.objects.exclude(other__exact="")
    for i in r:
        for s in i.other.split(";"):
            data[s.strip()] = i.cn
    return JsonResponse(
        data,
        safe=True,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
