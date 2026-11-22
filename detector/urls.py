"""
URL patterns for the Language Recognizer application.
"""

from django.urls import path
from . import views

app_name = "detector"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/detect/", views.detect_api, name="detect_api"),
    path("api/languages/", views.languages_api, name="languages_api"),
    path("api/health/", views.health_check, name="health_check"),
]
