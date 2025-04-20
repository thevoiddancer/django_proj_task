from django import forms
from .models import Korisnik, Smjer
from django.contrib.auth.hashers import make_password

class KorisnikCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Korisnik
        fields = ['ime', 'prezime', 'email', 'password']

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
        user.tip_korisnika = 'user'
        if commit:
            user.save()
        return user


class KorisnikLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import Prijava
from django.core.exceptions import ValidationError

class PrijavaForm(forms.ModelForm):
    class Meta:
        model = Prijava
        fields = [
            'smjer', 
            'datum_rođenja', 
            'mjesto_rođenja', 
            'završena_škola', 
            'molba', 
            'dokument', 
            'prosjek_ocjena', 
            'ocjena_matura'
        ]
        widgets = {
            'datum_rođenja': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        print("vrijednosti")
        print(args)
        print(kwargs)
        smjer = kwargs.pop('smjer', None)
        smjer_object = Smjer.objects.get(naziv=smjer)
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        # self.fields['smjer'] = forms.ModelChoiceField(
        #     queryset=Smjer.objects.all(),
        #     empty_label="Select a Smjer",
        #     to_field_name="naziv",  # Display the 'naziv' of the Smjer in the dropdown
        #     widget=forms.Select(attrs={'class': 'form-control'})
        # )            
        if smjer_object:
            print("imam smjer")
            print(self.fields['smjer'])
            self.fields['smjer'].initial = smjer_object.id
            self.fields['smjer'].widget = forms.HiddenInput()  # Make the smjer field hidden
            self.smjer_label = smjer  # Store smjer's naziv as a label to display


        if user:
            self.instance.korisnik = user

    def validate_file_upload(self):
        molba = self.cleaned_data.get('molba')
        if molba:
            # Only allow PDF files for molba
            if not molba.name.endswith('.pdf'):
                raise ValidationError('Molba must be a PDF file.')
            if molba.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Molba file size must be less than 5MB.')
        return molba

    def clean_molba(self):
        return self.validate_file_upload()

    def clean_dokument(self):
        return self.validate_file_upload()

    prosjek_ocjena = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))
    ocjena_matura = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))