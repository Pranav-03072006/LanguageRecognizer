"""
Root URL configuration for Language Recognizer application.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("detector.urls")),
]
