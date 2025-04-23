from django.urls import path

from . import views

urlpatterns = [
    path("saikai/resident", views.saikai_resident, name="saikai_resident"),
    path("saikai/festival", views.saikai_festival, name="saikai_festival"),
    path("saikai/cookbook", views.saikai_cookbook, name="saikai_cookbook"),
]
