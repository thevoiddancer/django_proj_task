from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Avg, Max, Min
from django.utils.dateparse import parse_date

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import CurrentStateSerializer, ExpenseByCategorySerializer, UserRegisterSerializer, ExpenseSerializer, IncomeSerializer, CategorySerializer, StatsByYearSerializer
from .models import Expense, Income, Category

def home(request):
    return HttpResponse("Welcome to API task using Django.<br />(c) Tomislav Nazifović")

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ovdje sam omogućio unošenje više kategorija, ali to me gurnulo u crnu rupu debate
        # kako napraviti da parametri butu safe što se tiče jedne ili više vrijednosti
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        date_year = self.request.query_params.get('date_year')
        date_month = self.request.query_params.get('date_month')
        date_day = self.request.query_params.get('date_day')
        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')
        cat_title = self.request.query_params.getlist('cat_title')
        cat_num = self.request.query_params.getlist('cat_num')
       
        expenses = Expense.objects
        if date_from:
            expenses = expenses.filter(date__gte=parse_date(date_from))
            print('date_from set')
        if date_to:
            expenses = expenses.filter(date__lte=parse_date(date_to))
            print('date_to set')
        if date_year:
            expenses = expenses.filter(date__year=date_year)
            print('date_year set')
        if date_month:
            expenses = expenses.filter(date__month=date_month)
            print('date_month set')
        if date_day:
            expenses = expenses.filter(date__day=date_day)
            print('date_day set')
        if amount_min:
            expenses = expenses.filter(amount__gte=amount_min)
            print('amount_min set')
        if amount_max:
            expenses = expenses.filter(amount__lte=amount_max)
            print('amount_max set')
        if cat_title:
            expenses = expenses.filter(category__title__in=cat_title)
            print('cat_title set')
        if cat_num:
            expenses = expenses.filter(category__in=cat_num)
            print('cat_num set')

        return expenses
        # return Expense.objects.filter(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter("date_from", OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description="Start date"),
            OpenApiParameter("date_to", OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description="End date"),
            OpenApiParameter("date_year", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Year of entry"),
            OpenApiParameter("date_month", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Month of entry"),
            OpenApiParameter("date_day", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Day of entry"),
            OpenApiParameter("amount_min", OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description="Minimum amount"),
            OpenApiParameter("amount_max", OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description="Maximum amount"),
            OpenApiParameter("cat_title", OpenApiTypes.STR, location=OpenApiParameter.QUERY, many=True, description="List of categories by name"),
            OpenApiParameter("cat_num", OpenApiTypes.INT, location=OpenApiParameter.QUERY, many=True, description="List of categories by number"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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

    @extend_schema(responses=StatsByYearSerializer)
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
