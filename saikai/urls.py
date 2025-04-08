from django.urls import path

from . import views

urlpatterns = [
    path("fish/", views.get_fish, name="fish"),
    path("cookbook/", views.get_cookbook, name="cookbook"),
    path("resident/", views.get_resident, name="resident_list"),
    path("resident/<str:r>/", views.get_resident, name="resident"),
]
