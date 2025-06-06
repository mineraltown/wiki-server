from django.contrib import admin
from .models import *


# 管理页面顶部的文字
admin.site.site_header = "矿石镇的攻略百科"
#  <title> （字符串）末尾放置的文字。
admin.site.site_title = "矿石镇的攻略百科"
# 管理索引页顶部的文字（一个字符串）
admin.site.index_title = "内容管理系统"


@admin.register(version)
class versionAdmin(admin.ModelAdmin):
    list_display = ["title", "title_jp", "sub", "release_date", "enable"]
    list_editable = ["enable"]
    list_filter = ["enable"]
    search_fields = ["title", "sub"]
    ordering = ["release_date"]


@admin.register(to)
class toAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]
    list_display = [
        "__str__",
        "sort",
        "version",
        "parent",
        "title",
        "link",
        "page",
        "enable",
    ]
    list_editable = ["enable"]
    list_filter = ["version", "enable"]
    autocomplete_fields = ["parent", "link"]


@admin.register(content)
class contentAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]


@admin.register(translate)
class translateAdmin(admin.ModelAdmin):
    search_fields = ["jp", "cn", "other"]
    list_display = ["jp", "cn", "other"]
