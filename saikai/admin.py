from django.contrib import admin
from .models import *


@admin.register(resident)
class residentAdmin(admin.ModelAdmin):
    list_display = ["name", "form", "sex", "birth_month", "birth_day"]
    list_filter = ["form", "sex", "birth_month"]
    search_fields = ["name", "name_jp", "name_en"]


@admin.register(fish)
class fishAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "min_size", "max_size", "king", "special", "trash"]
    list_filter = ["level", "king", "special", "trash"]
    search_fields = ["name"]


@admin.register(cookbook)
class cookbookAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "ingredients", "kitchenware"]
    search_fields = ["name", "ingredients", "kitchenware"]


@admin.register(event)
class eventAdmin(admin.ModelAdmin):
    list_display = ["title", "form"]
    search_fields = ["title"]
