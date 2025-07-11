from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Income/expense categories. Can take other categories as parents, to create subcategories.
    Both category and subcategory can be used as item category and as a parent."""

    class Meta:
        verbose_name_plural = "Categories"

    class CategoryType(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    title: models.CharField = models.CharField(max_length=100)
    type: models.CharField = models.CharField(
        max_length=7,
        choices=CategoryType.choices,
        default=CategoryType.EXPENSE,
    )
    parent: models.ForeignKey = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.parent} -> {self.title}" if self.parent else self.title


class Expense(models.Model):
    """Expense items."""

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    title: models.CharField = models.CharField(max_length=200)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    category: models.ForeignKey = models.ForeignKey(Category, on_delete=models.CASCADE)
    date: models.DateTimeField = models.DateTimeField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)


class Income(models.Model):
    """Income items."""

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    title: models.CharField = models.CharField(max_length=200)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    category: models.ForeignKey = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    date: models.DateTimeField = models.DateTimeField(default=timezone.now)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
