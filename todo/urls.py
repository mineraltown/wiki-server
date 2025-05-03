from django.urls import path
from . import views

urlpatterns = [
    path("saikai/resident", views.saikai_resident, name="saikai_resident"),
    path("saikai/festival", views.saikai_festival, name="saikai_festival"),
    path("saikai/cookbook", views.saikai_cookbook, name="saikai_cookbook"),
    path("<str:ver>/resident", views.Resident, name="Resident"),
    path("<str:ver>/festival", views.Festival, name="Festival"),
]
