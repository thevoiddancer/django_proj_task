from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import KorisnikLoginForm
from .models import Korisnik
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

home_list = [
    {
        'title': 'Tehnološki',
        'content': 'Kvota: 20',
    },
    {
        'title': 'Informatički',
        'content': 'Kvota: 120',
    },
    {
        'title': 'Matematički',
        'content': 'Kvota: 10',
    },
]

# Create your views here.
def home(request):
    context = {
        'posts': home_list,
    }
    return render(request, 'upis/home.html', context=context)

from django.db.models.query import QuerySet
from django.views.generic import ListView
import typing as tp
from .models import Smjer

class SmjeroviListView(ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        lista_smjerova = Smjer.objects.all()
        return lista_smjerova
    
    def get_context_data(self):
        context = super().get_context_data()
        return context

class PredmetiListView(ListView):
    def get_queryset(self) -> QuerySet[tp.Any]:
        self.smjer = self.kwargs.get('smjer', None)
        smjer_obj = Smjer.objects.get(naziv=self.smjer)
        lista_predmeta = smjer_obj.predmeti.all()
        return lista_predmeta
    
    def get_context_data(self):
        context = super().get_context_data()
        context['smjer'] = self.smjer
        return context


from django.contrib import messages
from .forms import KorisnikCreationForm

def register(request):
    if request.method == "POST":
        form = KorisnikCreationForm(request.POST)
        if form.is_valid():
            korisnik = form.save()
            messages.success(request, f'Account created for {korisnik.ime} {korisnik.prezime}')
            return redirect('login')
    else:
        form = KorisnikCreationForm()
    return render(request, 'upis/register.html', {'form': form})


def korisnik_login(request):
    if request.method == 'POST':
        form = KorisnikLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            korisnik = authenticate(request, email=email, password=password)
            if korisnik:
                login(request, korisnik, backend='upis.auth.KorisnikBackend')
                messages.success(request, f"Welcome back, {korisnik.ime}!")
                return redirect('upis-home')  # Update with your desired route
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = KorisnikLoginForm()
    return render(request, 'upis/login.html', {'form': form})


def korisnik_logout(request):
    logout(request)
    # messages.success(request, "You have been logged out.")
    return render(request, 'upis/logout.html')

@login_required
def user_admin(request):
    return render(request, 'upis/user_admin.html')

from django.shortcuts import render, redirect
from .forms import PrijavaForm

@login_required
def prijava_view(request, smjer=None):
    if request.method == 'POST':
        form = PrijavaForm(request.POST, request.FILES, user=request.user, smjer=smjer)
        print("validnost forma", form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('success')  # Replace 'success' with the actual name of your success page.
        else:
            print(form.errors)
    else:
        form = PrijavaForm(user=request.user, smjer=smjer)

    return render(request, 'upis/prijava.html', {'form': form})
