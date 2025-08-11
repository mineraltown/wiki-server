from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import *

CHECHE_TIME = 60 * 60 * 24 * 365 * 10  # 缓存10年

@cache_page(CHECHE_TIME)
def get_fish(request):
    data = []
    for i in fish.objects.all().order_by("id"):

        location = []
        if i.trash:
            location.append("全部")
        else:
            for x in i.location_list:
                if i.location_list[x]:
                    location.append(x)

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
                "location": location,
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


@cache_page(CHECHE_TIME)
def get_cookbook(request):
    data = []
    for i in cookbook.objects.all().order_by("id"):
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
