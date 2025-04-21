from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .models import Korisnik, Odobrenje, Prijava, Smjer


class KorisnikForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )


class KorisnikEditForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = [
            "ime",
            "prezime",
            "email",
            "is_staff",
            "is_superuser",
            "tip_korisnika",
        ]


class KorisnikCreationForm(KorisnikForm):
    class Meta:
        model = Korisnik
        fields = ["ime", "prezime", "email"]

    def __init__(self, *args, **kwargs):
        self.is_admin = kwargs.pop("is_admin", False)
        super().__init__(*args, **kwargs)

        if self.is_admin:
            self.fields["is_staff"] = forms.BooleanField(
                required=False, label="Is Staff"
            )
            self.fields["is_superuser"] = forms.BooleanField(
                required=False, label="Is Superuser"
            )
            self.fields["tip_korisnika"] = forms.ChoiceField(
                choices=Korisnik._meta.get_field("tip_korisnika").choices,
                label="Tip korisnika",
            )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("password_confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password_hash = make_password(self.cleaned_data["password"])

        if self.is_admin:
            user.is_staff = self.cleaned_data.get("is_staff", False)
            user.is_superuser = self.cleaned_data.get("is_superuser", False)
            user.tip_korisnika = self.cleaned_data.get("tip_korisnika")
        else:
            user.tip_korisnika = "user"

        if commit:
            user.save()
        return user


class OdobrenjeForm(forms.ModelForm):
    class Meta:
        model = Odobrenje
        fields = ["objasnjenje"]

    def __init__(self, *args, **kwargs):
        self.prijava_id = kwargs.pop("prijava_id", None)
        self.upisnik_id = kwargs.pop("upisnik_id", None)
        super().__init__(*args, **kwargs)

    def save(self, comit=True):
        odobrenje = super().save(commit=False)
        odobrenje.prijava_id = self.prijava_id
        odobrenje.vrijeme = now()
        odobrenje.upisnik_id = self.upisnik_id

        if comit:
            odobrenje.save()
        return odobrenje


class KorisnikLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)


class PrijavaForm(forms.ModelForm):
    class Meta:
        model = Prijava
        fields = [
            "smjer",
            "datum_rođenja",
            "mjesto_rođenja",
            "završena_škola",
            "molba",
            "dokument",
            "prosjek_ocjena",
            "ocjena_matura",
        ]
        widgets = {
            "datum_rođenja": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        smjer = kwargs.pop("smjer", None)
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if smjer:
            smjer_object = Smjer.objects.get(naziv=smjer)
            self.fields["smjer"].initial = smjer_object.id
            self.fields["smjer"].widget = forms.HiddenInput()
            self.smjer_label = smjer

        if user:
            self.instance.korisnik = user

            prijave = Prijava.objects.filter(korisnik_id=user.id)
            prijave_ids = [p.smjer_id for p in prijave]

            available_smjerovi = Smjer.objects.exclude(id__in=prijave_ids)
            self.fields["smjer"].queryset = available_smjerovi

    def validate_file_upload(self):
        file = self.cleaned_data.get("file")
        if file:
            if not file.name.endswith(".pdf"):
                raise ValidationError("Dokument mora biti tipa PDF.")
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Dokument mora biti manji od 5MB.")
        return file

    def clean_molba(self):
        return self.validate_file_upload()

    def clean_dokument(self):
        return self.validate_file_upload()
