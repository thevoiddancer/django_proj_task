import typing as tp

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    KorisnikCreationForm,
    KorisnikEditForm,
    KorisnikLoginForm,
    OdobrenjeForm,
    PrijavaForm,
)
from .models import Korisnik, Odobrenje, Prijava, Smjer


# Originalno sam kreirao ove viewove pa se poslije prebacio na CBV.
# Iskreno ne znam zašto, ali se nikad nisam vratio da ovo ujednačim.
# TODO: to CBV
def register(request):
    if request.method == "POST":
        form = KorisnikCreationForm(request.POST)
        if form.is_valid():
            korisnik = form.save()
            messages.success(
                request, f"Account created for {korisnik.ime} {korisnik.prezime}"
            )
            return redirect("login")
    else:
        form = KorisnikCreationForm()
    return render(request, "upis/register.html", {"form": form})


# TODO: to CBV
def korisnik_login(request):
    if request.method == "POST":
        form = KorisnikLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            korisnik = authenticate(request, email=email, password=password)
            if korisnik:
                login(request, korisnik, backend="upis.auth.KorisnikBackend")
                messages.success(request, f"Dobrodošao, {korisnik.ime}!")
                return redirect("upis-home")  # Update with your desired route
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = KorisnikLoginForm()
    return render(request, "upis/login.html", {"form": form})


# TODO: to CBV
def korisnik_logout(request):
    logout(request)
    return render(request, "upis/logout.html")


@login_required
def prijava_view(request, smjer=None):
    if request.method == "POST":
        form = PrijavaForm(request.POST, request.FILES, user=request.user, smjer=smjer)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Prijava na {form.cleaned_data.get('smjer')} uspješno zabilježena.",
            )
            return redirect(
                "upis-home"
            )  # Replace 'success' with the actual name of your success page.
    else:
        form = PrijavaForm(user=request.user, smjer=smjer)

    return render(request, "upis/prijava.html", {"form": form})


@staff_member_required
def prijave(request):
    return render(request, "upis/prijave.html")


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(self.request.get_full_path())


class KorisnikDeleteView(StaffRequiredMixin, DeleteView):
    model = Korisnik
    template_name = "upis/korisnik_confirm_delete.html"
    success_url = reverse_lazy("korisnici")


class KorisnikEditView(StaffRequiredMixin, UpdateView):
    model = Korisnik
    form_class = KorisnikEditForm
    template_name = "upis/korisnik_edit.html"
    success_url = reverse_lazy("korisnici")


################
# Create views #
################


class KorisnikCreateView(StaffRequiredMixin, CreateView):
    """Stvara nove korisnike.

    is_admin se šalje ako ga se stvara iz admin sučelja, pa se može stvoriti i admin korisnik."""

    model = Korisnik
    form_class = KorisnikCreationForm
    template_name = "upis/korisnik_novi.html"
    success_url = reverse_lazy("korisnici")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_admin"] = True
        return kwargs


class OdobriView(StaffRequiredMixin, CreateView):
    """Stvara novi objekt Odobrenje.

    Broj prijave i id korisnika koji je odobrio se proslijeđuju formu."""

    model = Odobrenje
    form_class = OdobrenjeForm
    template_name = "upis/odobri.html"
    success_url = reverse_lazy("prijave")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["prijava_id"] = self.kwargs.pop("pk", None)
        kwargs["upisnik_id"] = self.request.user.id
        return kwargs


##############
# List views #
##############


class PrijaveListView(StaffRequiredMixin, ListView):
    """Prikazuje sve prijave."""

    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Prijava.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        return context


class KorisniciListView(StaffRequiredMixin, ListView):
    """Prikazuje sve korisnike."""

    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Korisnik.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        return context


class SmjeroviListView(ListView):
    """Prikazuje sve smjerove.

    Dodatno provjeri na koje smjerove se osoba još može prijaviti.
    """

    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Smjer.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        korisnik = self.request.user
        prijave = Prijava.objects.filter(korisnik_id=korisnik.id)
        prijave_ids = [p.smjer_id for p in prijave]
        lista_smjerova = Smjer.objects.all()
        vec_odobren = Odobrenje.objects.filter(
            prijava__korisnik__id=korisnik.id
        ).exists()

        available_smjerovi = lista_smjerova.exclude(id__in=prijave_ids)
        context["dostupni_smjerovi"] = available_smjerovi and not vec_odobren
        context["moze_prijaviti"] = available_smjerovi.exists()
        return context


class PredmetiListView(ListView):
    """Prikazuje predmete koji se nalaze na određenom smjeru.

    Dodatno, provjerava je li se osoba već prijavila za smjer prije nego ponudi opciju prijave.
    """

    def get_queryset(self) -> QuerySet[tp.Any]:
        self.smjer = self.kwargs.get("smjer", None)
        self.smjer_obj = Smjer.objects.get(naziv=self.smjer)
        lista_predmeta = self.smjer_obj.predmeti.all()
        return lista_predmeta

    def get_context_data(self):
        context = super().get_context_data()
        context["smjer"] = self.smjer
        korisnik = self.request.user
        prijava = Prijava.objects.filter(
            korisnik_id=korisnik.id, smjer_id=self.smjer_obj.id
        )
        može_prijaviti = len(prijava) == 0
        vec_odobren = Odobrenje.objects.filter(
            prijava__korisnik__id=korisnik.id
        ).exists()
        context["moze_prijaviti"] = može_prijaviti and not vec_odobren
        return context


class OdobrenjaListView(StaffRequiredMixin, ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Odobrenje.objects.all()
        return lista_smjerova
