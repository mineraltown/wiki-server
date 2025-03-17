from django.http import JsonResponse
from .models import *


def get_resident(request, r=False):
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
            "desc": i.desc.replace("\r\n", ""),
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
            "note": i.note.replace("\r\n", ""),
            "event": {},
        }

        for x in EVENT_CLASSIFICATION:
            if x[0] == "L":
                data["event"][x[1]] = []
                # r = event.objects.filter(performer=i, form=x[0])
                r = event.objects.filter(performer=i, form=x[0])
                print(r)
                for e in r:
                    print(e)
                    n = {
                        "title": e.title,
                        "desc": e.desc.replace("\r\n", ""),
                        "date": e.date,
                        "week": e.week,
                        "time": e.time,
                        "weather": e.weather,
                        "address": e.address,
                        "other": e.other.replace("\r\n", ""),
                        "performer": list(e.performer.values_list("name", flat=True)),
                        "result": e.result.replace("\r\n", ""),
                        "note": e.note.replace("\r\n", ""),
                    }
                    data["event"][x[1]].append(n)
            else:
                data["event"][x[1]] = list(
                    event.objects.filter(performer=i, form=x[0]).values_list(
                        "id", "title"
                    )
                )

        if i.birth_day_another != 0 and i.birth_day_another != i.birth_day:
            data["birth"]["another"] = i.birth_day_another

    else:
        for x in CLASSIFICATION:
            data[x[1]] = {}
            for y in resident.objects.filter(form=x[0]):
                data[x[1]][y.name_en] = {"icon": y.icon.url, "name": y.name}

    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def get_fish(request):
    data = []
    for i in fish.objects.all():
        data.append(
            {
                "name": i.name,
                "level": i.level,
                "season": {
                    "spring": i.spring,
                    "summer": i.summer,
                    "autumn": i.autumn,
                    "winter": i.winter,
                },
                "location_list": i.location_list,
                "size": {
                    "min": i.min_size,
                    "max": i.max_size,
                },
                "king": i.king,
                "special": i.special,
                "trash": i.trash,
                "note": i.note,
            }
        )
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def get_event(request, mode=False):
    data = []
    if mode:
        r = event.objects.filter(form=mode)
        for i in r:
            n = {
                "title": i.title,
                "desc": i.desc.replace("\r\n", ""),
                "time": i.time,
                "weather": i.weather,
                "address": i.address,
                "other": i.other.replace("\r\n", ""),
                "performer": list(i.performer.values_list("name", flat=True)),
                "result": i.result.replace("\r\n", ""),
                "note": i.note.replace("\r\n", ""),
            }
            if mode == "E":
                n["month"] = i.month
                n["day"] = i.day
            else:
                n["date"] = i.date
                n["week"] = i.week
            data.append(n)
    else:
        data = EVENT_CLASSIFICATION
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )


def get_cookbook(request):
    data = []
    for i in cookbook.objects.all():
        data.append(
            {
                "name": i.name,
                "price": i.price,
                "physical": i.physical,
                "fatigue": i.fatigue,
                "ingredients": i.ingredients,
                "kitchenware": i.kitchenware,
                "how_to_get": i.how_to_get,
            }
        )
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
