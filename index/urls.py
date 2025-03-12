from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("version/", views.ver, name="version"),
    path("html/", views.html, name="html"),
]
