from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from upis.models import Korisnik


class KorisnikBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            korisnik = Korisnik.objects.get(email=email)
            if check_password(password, korisnik.password_hash):
                return korisnik
        except Korisnik.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Korisnik.objects.get(pk=user_id)
        except Korisnik.DoesNotExist:
            return None
