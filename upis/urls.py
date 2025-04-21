from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.SmjeroviListView.as_view(), name="upis-home"),
    path("prijava/", views.prijava_view, name="prijava"),
    path("prijava/<str:smjer>", views.prijava_view, name="prijava"),
    path("korisnici/", views.KorisniciListView.as_view(), name="korisnici"),
    path(
        "korisnici/delete/<int:pk>",
        views.KorisnikDeleteView.as_view(),
        name="korisnici-delete",
    ),
    path("korisnici/novi", views.KorisnikCreateView.as_view(), name="korisnici-novi"),
    path(
        "korisnici/edit/<int:pk>/",
        views.KorisnikEditView.as_view(),
        name="korisnici-edit",
    ),
    path("prijave/", views.PrijaveListView.as_view(), name="prijave"),
    path("odobri/<int:pk>", views.OdobriView.as_view(), name="odobri"),
    path("odobrenja/", views.OdobrenjaListView.as_view(), name="odobrenja"),
    path("admin/", admin.site.urls),
    path("login/", views.korisnik_login, name="login"),
    path("logout/", views.korisnik_logout, name="logout"),
    path("register/", views.register, name="register"),
    path(
        "predmeti/<str:smjer>/", views.PredmetiListView.as_view(), name="predmeti_list"
    ),
]
