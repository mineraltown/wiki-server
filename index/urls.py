from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.menu, name="version"),
    path("menu/<str:v>/", views.menu, name="menu"),
    path("html/<int:id>", views.html, name="html"),
]
