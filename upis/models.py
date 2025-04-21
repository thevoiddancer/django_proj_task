from .managers import KorisnikManager  
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Predmet(models.Model):
    naziv = models.CharField(max_length=100, null=False, blank=False)
    opis = models.CharField(max_length=200, null=False, blank=False)
    nositelj = models.CharField(max_length=100, null=False, blank=False)
    ects = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'predmeti'
        ordering = ['naziv']
        verbose_name = 'Predmet'
        verbose_name_plural = 'Predmeti'
    
    def __repr__(self):
        return self.naziv

class Smjer(models.Model):
    naziv = models.CharField(max_length=100, null=False, blank=False)
    kvota = models.IntegerField(null=False, blank=False)
    slobodno = models.IntegerField(null=False, blank=False)
    predmeti = models.ManyToManyField('Predmet', related_name='smjerovi')

    class Meta:
        db_table = 'smjerovi'
        ordering = ['naziv']
        verbose_name = 'Smjer'
        verbose_name_plural = 'Smjerovi'

    def __repr__(self):
        return self.naziv

    def __str__(self):
        return self.naziv

class Korisnik(AbstractBaseUser, PermissionsMixin):
    ime = models.CharField(max_length=100, null=False, blank=False)
    prezime = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=255, null=False, blank=False)

    TIP_KORISNIKA = [
        ('admin', 'Administrator'),
        ('user', 'Student'),
    ]
    tip_korisnika = models.CharField(max_length=20, choices=TIP_KORISNIKA, default='user')

    USERNAME_FIELD = 'email'  # used to log in
    REQUIRED_FIELDS = ['ime', 'prezime']  # asked when creating superuser
    objects = KorisnikManager()  # required
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = 'korisnici'
        ordering = ['prezime', 'ime']
        verbose_name = 'Korisnik'
        verbose_name_plural = 'Korisnici'

    def __repr__(self):
        return f'{self.ime} {self.prezime}'

class Prijava(models.Model):
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=False, blank=False)
    smjer = models.ForeignKey(Smjer, on_delete=models.CASCADE, null=False, blank=False)
    datum_rođenja = models.DateField(null=False, blank=False)
    mjesto_rođenja = models.CharField(max_length=100, null=False, blank=False)
    završena_škola = models.CharField(max_length=100, null=False, blank=False)
    molba = models.FileField(upload_to='molbe/', null=True, blank=True)
    dokument = models.FileField(upload_to='dokumenti/', null=True, blank=True)
    prosjek_ocjena = models.FloatField(null=True, blank=True)
    ocjena_matura = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'prijave'
        verbose_name = 'Prijava'
        verbose_name_plural = 'Prijave'

        constraints = [
            models.UniqueConstraint(fields=['korisnik', 'smjer'], name='unique_korisnik_smjer')
        ]

    def __repr__(self):
        return f'{self.korisnik.prezime} > {self.smjer.naziv}'

class Upis(models.Model):
    # TODO: implementirati logiku tako da se spremi informacija u slučaju brisanja entrya
    # možda spremiti podatke u obliku jsona za studenta i upisnika?
    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name='student', null=False, blank=False)
    upisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name='upisnik', null=False, blank=False)
    vrijeme_odobrenja = models.DateTimeField(null=False, blank=False)
    objasnjenje_odobrenja = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'upisi'
        verbose_name = 'Upis'
        verbose_name_plural = 'Upisi'
    
    def __repr__(self):
        return f'{self.student.prezime} [upisao: {self.upisnik.prezime}]'