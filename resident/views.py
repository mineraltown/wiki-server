from django.http import JsonResponse
from saikai.models import resident, CLASSIFICATION


def saikai_resident(request, r=False):
    data = {}
    if r:
        i = resident.objects.get(name_en=r)
        data = {
            "name": {
                "cn": i.name,
                "jp": i.name_jp,
                "en": i.name_en,
            },
            "photo": i.photo.url,
            "desc": i.desc.replace("\r\n", "").replace(
                'src="/static/', f"src=\"{request.build_absolute_uri('/')[:-1]}/static/"
            ),
            "first": i.first,
            "address": i.address,
            "sex": i.get_sex_display(),
            "birth": {
                "month": i.get_birth_month_display(),
                "day": i.birth_day,
            },
            "family": i.family,
            "like": i.like,
            "trip": i.trip.replace("\r\n", ""),
            "note": i.note.replace("\r\n", "").replace(
                'src="/static/', f"src=\"{request.build_absolute_uri('/')[:-1]}/static/"
            ),
        }
        if i.birth_day_another != 0 and i.birth_day_another != i.birth_day:
            data["birth"]["another"] = i.birth_day_another

    else:
        for x in CLASSIFICATION:
            data[x[1]] = {}
            for y in resident.objects.filter(form=x[0]).order_by("id"):
                data[x[1]][y.name_en] = {"icon": y.icon.url, "name": y.name}

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
