from django.urls import path

from . import views

urlpatterns = [
    path("resident/", views.get_resident, name="resident_list"),
    path("resident/<str:r>/", views.get_resident, name="resident"),
]
