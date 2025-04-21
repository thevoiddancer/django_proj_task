import typing as tp

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    KorisnikCreationForm,
    KorisnikEditForm,
    KorisnikLoginForm,
    OdobrenjeForm,
    PrijavaForm,
)
from .models import Korisnik, Odobrenje, Prijava, Smjer


# to CBV
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


# to CBV
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


# to CBV
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


class KorisniciListView(StaffRequiredMixin, ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Korisnik.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        return context


class PrijaveListView(StaffRequiredMixin, ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Prijava.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        return context


class KorisnikDeleteView(StaffRequiredMixin, DeleteView):
    model = Korisnik
    template_name = "upis/korisnik_confirm_delete.html"
    success_url = reverse_lazy(
        "korisnici"
    )  # Redirect back to korisnici list after deletion


class KorisnikCreateView(StaffRequiredMixin, CreateView):
    model = Korisnik
    form_class = KorisnikCreationForm
    template_name = "upis/korisnik_novi.html"
    success_url = reverse_lazy("korisnici")  # Redirect after successful creation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_admin"] = True  # Pass to the form constructor
        return kwargs


class KorisnikEditView(StaffRequiredMixin, UpdateView):
    model = Korisnik
    form_class = KorisnikEditForm
    template_name = "upis/korisnik_edit.html"
    success_url = reverse_lazy("korisnici")  # Redirect after successful creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = (
            "Edit"  # Add a flag for the template to know it's an edit action
        )
        return context


class OdobriView(StaffRequiredMixin, CreateView):
    model = Odobrenje
    form_class = OdobrenjeForm
    template_name = "upis/odobri.html"

    def dispatch(self, request, *args, **kwargs):
        self.prijava = get_object_or_404(Prijava, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.prijava = self.prijava
        form.instance.upisnik = self.request.user
        form.instance.vrijeme = now()
        valid_form = super().form_valid(form)

        # korisnik = self.prijava.korisnik
        # Prijava.objects.filter(korisnik=korisnik).exclude(pk=self.prijava.pk).delete()
        return valid_form

    def get_success_url(self):
        return reverse_lazy("prijave")  # or wherever you want to redirect


class SmjeroviListView(ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Smjer.objects.all()
        return lista_smjerova

    def get_context_data(self):
        context = super().get_context_data()
        korisnik = self.request.user
        prijave = Prijava.objects.filter(korisnik_id=korisnik.id)
        prijave_ids = [p.smjer_id for p in prijave]
        lista_smjerova = Smjer.objects.all()

        available_smjerovi = lista_smjerova.exclude(id__in=prijave_ids)
        context["dostupni_smjerovi"] = available_smjerovi
        context["moze_prijaviti"] = available_smjerovi.exists()
        return context


class PredmetiListView(ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        self.smjer = self.kwargs.get("smjer", None)
        print(self.smjer)
        self.smjer_obj = Smjer.objects.get(naziv=self.smjer)
        lista_predmeta = self.smjer_obj.predmeti.all()
        return lista_predmeta

    def get_context_data(self):
        context = super().get_context_data()
        context["smjer"] = self.smjer
        prijava = Prijava.objects.filter(
            korisnik_id=self.request.user.id, smjer_id=self.smjer_obj.id
        )
        može_prijaviti = len(prijava) == 0
        context["moze_prijaviti"] = može_prijaviti
        return context


class OdobrenjaView(StaffRequiredMixin, ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Odobrenje.objects.all()
        return lista_smjerova
