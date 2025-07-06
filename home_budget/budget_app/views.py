from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Avg, Max, Min

from drf_spectacular.utils import extend_schema
from .serializers import CurrentStateSerializer, ExpenseByCategorySerializer, UserRegisterSerializer, ExpenseSerializer, IncomeSerializer, CategorySerializer
from .models import Expense, Income, Category

def home(request):
    return HttpResponse("Welcome to API task using Django.<br />(c) Tomislav Nazifović")

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=UserRegisterSerializer, responses=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            Income.objects.create(
                user=user,
                title="Starting Balance",
                amount=1000,
                category=None
            )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    # "user": UserRegisterSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatsByYearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, year):
        expenses_stats = Expense.objects.filter(
            user=request.user,
            created_at__year=year
        ).aggregate(
            min_amount=Min('amount'),
            max_amount=Max('amount'),
            avg_amount=Avg('amount')
        )

        incomes_stats = Income.objects.filter(
            user=request.user,
            created_at__year=year
        ).aggregate(
            min_amount=Min('amount'),
            max_amount=Max('amount'),
            avg_amount=Avg('amount')
        )

        expenses_stats = {k: v or 0 for k, v in expenses_stats.items()}
        incomes_stats = {k: v or 0 for k, v in incomes_stats.items()}

        agg_stats_by_year = {'year': year, 'expenses': expenses_stats, 'incomes': incomes_stats}

        return Response(agg_stats_by_year)
    
class ExpenseByCategoryView(APIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        expenses = Expense.objects.filter(
            user=request.user,
            category__id=pk
        )

        serializer = self.serializer_class(expenses, many=True)
        return Response(serializer.data)

class IncomeByCategoryView(APIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        incomes = Income.objects.filter(
            user=request.user,
            category__id=pk
        )

        serializer = self.serializer_class(incomes, many=True)
        return Response(serializer.data)

class CurrentStateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=CurrentStateSerializer)
    def get(self, request):
        total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'current_balance': total_income - total_expense
        })
