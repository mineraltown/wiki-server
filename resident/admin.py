from django.contrib import admin
from .models import *


@admin.register(resident)
class residentAdmin(admin.ModelAdmin):
    list_display = ["name", "form", "version"]
    list_filter = ["form", "version"]
    search_fields = ["name", "name_jp", "name_en"]
