from django.template import loader
from django.http import JsonResponse
from saikai.models import resident, CLASSIFICATION


def saikai_resident(request, id=False):
    data = {}
    if id:
        i = resident.objects.get(id=id)
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
            for y in resident.objects.filter(form=x[0]).order_by("id"):
                data[x[1]][y.name_en] = {"id": y.id, "icon": y.icon.url, "name": y.name}

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
