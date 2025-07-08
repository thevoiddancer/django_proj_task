from django.contrib import admin
from django.urls import include, path

from budget_app.views import home

urlpatterns = [
    path("", home),
    path("admin", admin.site.urls),
    path("api/", include("budget_app.urls")),
]
