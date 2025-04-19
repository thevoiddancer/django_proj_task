from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import KorisnikLoginForm
from .models import Korisnik
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

home_list = [
    {
        'title': 'About',
        'content': 'SamplesAbyss is an attempt to resurrect (or at least reincarnate) the old website of samples.sloth org.',
    },
    {
        'title': 'Stats',
        'content': 'Statistics about the page.',
    },
    {
        'title': 'TODO - in order',
        'content': 'Implement formatting for data. Implement breadcrumbs (how to fix it when on samples page?). Implement IMDB/Spotify/Discogs API. Fix data (compilations etc). Implement search function. Implement contribute function.',
    },
    {
        'title': 'Top-of-the-line',
        'content': 'I guess I could select top artist and top source here?',
    },
    {
        'title': 'Spotlight',
        'content': 'I guess I could spotlight an artist or source here? I could also do an "underdog" version?',
    },
    {
        'title': 'Latest addition',
        'content': 'Nothing to add here as of yet. Expand the database by adding date of addition and then query for last 5 entries here and show them in sample layout, I guess?',
    },
]

# Create your views here.
def home(request):
    context = {
        'posts': home_list,
    }
    return render(request, 'upis/home.html', context=context)

from django.contrib import messages
from .forms import KorisnikCreationForm

def register(request):
    if request.method == "POST":
        form = KorisnikCreationForm(request.POST)
        if form.is_valid():
            korisnik = form.save()
            messages.success(request, f'Account created for {korisnik.ime} {korisnik.prezime}')
            return redirect('upis-home')
    else:
        form = KorisnikCreationForm()
    return render(request, 'upis/register.html', {'form': form})


def korisnik_login(request):
    if request.method == 'POST':
        form = KorisnikLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email)
            print(password)
            korisnik = authenticate(request, email=email, password=password)
            print(korisnik)
            if korisnik:
                login(request, korisnik, backend='upis.auth.KorisnikBackend')
                messages.success(request, f"Welcome back, {korisnik.ime}!")
                return redirect('upis-home')  # Update with your desired route
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = KorisnikLoginForm()
    return render(request, 'upis/login.html', {'form': form})
