from rest_framework import serializers
from .models import Expense, Income, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['user']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'category': {'required': False, 'allow_null': True},
        }

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class CurrentStateSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_balance = serializers.DecimalField(max_digits=10, decimal_places=2)

class ExpenseByCategorySerializer(serializers.Serializer):
    category__name = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

