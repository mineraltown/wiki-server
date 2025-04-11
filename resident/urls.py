from django.urls import path

from . import views

urlpatterns = [
    path("saikai/", views.saikai_resident, name="saikai_resident_list"),
    path("saikai/<str:id>/", views.saikai_resident, name="saikai_resident"),
]
