from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Income/expense categories. Can take other categories as parents, to create subcategories.
    Both category and subcategory can be used as item category and as a parent."""
    class CategoryType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=7,
        choices=CategoryType.choices,
        default=CategoryType.EXPENSE,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.parent} -> {self.name}" if self.parent else self.name

class Expense(models.Model):
    """Expense items."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Income(models.Model):
    """Income items."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)