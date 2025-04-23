from django.http import JsonResponse
from saikai.models import resident, festival, tv_cookbook


def saikai_resident(request):
    data = []
    for i in resident.objects.all().order_by("id"):
        if i.birth_month != "N":
            if "最喜欢" in i.like:
                best = i.like["最喜欢"]
            else:
                best = []
            if "喜欢" in i.like:
                more = i.like["喜欢"]
            else:
                more = []
            data.append(
                {
                    "name": i.name,
                    "birthday": {
                        "month": i.get_birth_month_display(),
                        "day": i.birth_day,
                        "day2": (
                            None if i.birth_day_another == 0 else i.birth_day_another
                        ),
                    },
                    "like": {
                        "best": best,
                        "more": more,
                    },
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


def saikai_festival(request):
    data = []
    for i in festival.objects.all().order_by("id"):
        if i.note == "":
            note = None
        else:
            note = i.note
        data.append(
            {
                "name": i.name,
                "month": i.get_month_display(),
                "day": i.day,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "address": i.address,
                "note": note,
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


def saikai_cookbook(request):
    data = []
    for i in tv_cookbook.objects.all().order_by("id"):
        data.append(
            {
                "year": i.year,
                "month": i.get_month_display(),
                "day": i.day,
                "name": i.name,
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
