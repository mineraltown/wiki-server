from django.contrib import admin
from .models import *


@admin.register(resident)
class residentAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_month", "birth_day", "form", "version"]
    list_filter = ["form", "version"]
    search_fields = ["name", "name_jp", "name_en"]
