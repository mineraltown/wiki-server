from django.template import loader
from django.http import JsonResponse
from .models import *
from saikai.models import resident as saikai_resident_models

def get_resident(request, ver="", id=False):
    data = {}
    if id:
        i = resident.objects.get(id=id)
        i.note = i.note.replace(
            'src="/static/', f"src=\"{request.build_absolute_uri('/')[:-1]}/static/"
        )
        if i.photo:
            p = i.photo.url
        elif i.icon:
            p = i.icon.url
        else:
            p = ""
        data = {
            "name": i.name,
            "photo": p,
            "html": i.note,
        }
    else:
        for x in CLASSIFICATION:
            data[x[1]] = {}
            for y in resident.objects.filter(version__sub=ver, form=x[0]).order_by("id"):
                data[x[1]][y.name_en] = {"id": y.id, "icon": y.icon.url, "name": y.name}
            if len(data[x[1]]) == 0:
                data.pop(x[1])

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def saikai_resident(request, id=False):
    data = {}
    if id:
        i = saikai_resident_models.objects.get(id=id)
        i.note = i.note.replace(
            'src="/static/', f"src=\"{request.build_absolute_uri('/')[:-1]}/static/"
        )
        context = {
            "url": request.build_absolute_uri("/")[:-1],
            "resident": i,
        }
        template = loader.get_template("resident/saikai.html")
        data = {
            "name": i.name,
            "photo": i.photo.url,
            "html": template.render(context, request),
        }
    else:
        for x in CLASSIFICATION:
            data[x[1]] = {}
            for y in saikai_resident_models.objects.filter(form=x[0]).order_by("id"):
                data[x[1]][y.name_en] = {"id": y.id, "icon": y.icon.url, "name": y.name}
            if len(data[x[1]]) == 0:
                data.pop(x[1])

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
