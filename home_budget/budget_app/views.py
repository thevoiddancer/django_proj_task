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
from .serializers import CurrentStateSerializer, UserRegisterSerializer, ExpenseSerializer, IncomeSerializer, CategorySerializer, StatsByYearSerializer
from .models import Expense, Income, Category

def home(request):
    return HttpResponse("Welcome to API task using Django.<br />(c) Tomislav Nazifović")

KWORDS = ['name', 'type', 'location', 'description', 'many']
param_tuples = (
    ("date_from", OpenApiTypes.DATE, OpenApiParameter.QUERY, "Start date"),
    ("date_to", OpenApiTypes.DATE, OpenApiParameter.QUERY, "End date"),
    ("date_year", OpenApiTypes.INT, OpenApiParameter.QUERY, "Year of entry"),
    ("date_month", OpenApiTypes.INT, OpenApiParameter.QUERY, "Month of entry"),
    ("date_day", OpenApiTypes.INT, OpenApiParameter.QUERY, "Day of entry"),
    ("amount_min", OpenApiTypes.NUMBER, OpenApiParameter.QUERY, "Minimum amount"),
    ("amount_max", OpenApiTypes.NUMBER, OpenApiParameter.QUERY, "Maximum amount"),
    ("cat_title", OpenApiTypes.STR, OpenApiParameter.QUERY, "List of categories by name", True),
    ("cat_num", OpenApiTypes.INT, OpenApiParameter.QUERY, "List of categories by number", True),
)

common_query_parameters = [OpenApiParameter(**{k: v for k, v in zip(KWORDS, tuple_)}) for tuple_ in param_tuples]

# common_query_parameters = [
#     OpenApiParameter(name="date_from", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description="Start date"),
#     OpenApiParameter("date_to", OpenApiTypes.DATE, location=OpenApiParameter.QUERY, description="End date"),
#     OpenApiParameter("date_year", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Year of entry"),
#     OpenApiParameter("date_month", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Month of entry"),
#     OpenApiParameter("date_day", OpenApiTypes.INT, location=OpenApiParameter.QUERY, description="Day of entry"),
#     OpenApiParameter("amount_min", OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description="Minimum amount"),
#     OpenApiParameter("amount_max", OpenApiTypes.NUMBER, location=OpenApiParameter.QUERY, description="Maximum amount"),
#     OpenApiParameter("cat_title", OpenApiTypes.STR, location=OpenApiParameter.QUERY, many=True, description="List of categories by name"),
#     OpenApiParameter("cat_num", OpenApiTypes.INT, location=OpenApiParameter.QUERY, many=True, description="List of categories by number"),
# ]

def apply_query_filters(queryset, query_params):
    date_from = query_params.get('date_from')
    date_to = query_params.get('date_to')
    date_year = query_params.get('date_year')
    date_month = query_params.get('date_month')
    date_day = query_params.get('date_day')
    amount_min = query_params.get('amount_min')
    amount_max = query_params.get('amount_max')
    cat_title = query_params.getlist('cat_title')
    cat_num = query_params.getlist('cat_num')
    
    if date_from:
        queryset = queryset.filter(date__gte=parse_date(date_from))
    if date_to:
        queryset = queryset.filter(date__lte=parse_date(date_to))
    if date_year:
        queryset = queryset.filter(date__year=date_year)
    if date_month:
        queryset = queryset.filter(date__month=date_month)
    if date_day:
        queryset = queryset.filter(date__day=date_day)
    if amount_min:
        queryset = queryset.filter(amount__gte=amount_min)
    if amount_max:
        queryset = queryset.filter(amount__lte=amount_max)
    if cat_title:
        queryset = queryset.filter(category__title__in=cat_title)
    if cat_num:
        queryset = queryset.filter(category__in=cat_num)

    return queryset

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        queryset = apply_query_filters(queryset, self.request.query_params)
        return queryset

    @extend_schema(parameters=common_query_parameters)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Income.objects.filter(user=self.request.user)
        queryset = apply_query_filters(queryset, self.request.query_params)
        return queryset

    @extend_schema(parameters=common_query_parameters)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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

class CurrentBalanceView(APIView):
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
