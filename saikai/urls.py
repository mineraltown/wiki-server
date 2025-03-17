from django.urls import path

from . import views

urlpatterns = [
    path("fish/", views.get_fish, name="fish"),
    path("cookbook/", views.get_cookbook, name="cookbook"),
    path("event/", views.get_event, name="event_list"),
    path("event/<str:mode>", views.get_event, name="event"),
    path("resident/", views.get_resident, name="resident_list"),
    path("resident/<str:r>/", views.get_resident, name="resident"),
]
