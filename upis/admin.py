# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Korisnik


class KorisnikAdmin(UserAdmin):
    model = Korisnik
    list_display = ["email", "ime", "prezime", "tip_korisnika", "is_staff"]
    ordering = ["email"]
    search_fields = ["email"]
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Personal Info", {"fields": ("ime", "prezime")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Other Info", {"fields": ("tip_korisnika",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "ime",
                    "prezime",
                    "password1",
                    "password2",
                    "tip_korisnika",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(Korisnik, KorisnikAdmin)
