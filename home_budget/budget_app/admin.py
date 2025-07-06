from django.contrib import admin

# Register your models here.
from .models import Category, Expense, Income

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Income)
