import django
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Expense, Income
from .serializers import (
    CategorySerializer,
    CurrentBalanceSerializer,
    ExpenseSerializer,
    IncomeSerializer,
    StatsSerializer,
    UserRegisterSerializer,
)

STARTING_BALANCE = 1000


def home(request):
    return HttpResponse("Welcome to API task using Django.<br />(c) Tomislav Nazifović")


KWORDS = ["name", "type", "location", "description", "many"]
param_tuples = (
    ("date_from", OpenApiTypes.DATE, OpenApiParameter.QUERY, "Start date"),
    ("date_to", OpenApiTypes.DATE, OpenApiParameter.QUERY, "End date"),
    ("date_year", OpenApiTypes.INT, OpenApiParameter.QUERY, "Year of entry"),
    ("date_month", OpenApiTypes.INT, OpenApiParameter.QUERY, "Month of entry"),
    ("date_day", OpenApiTypes.INT, OpenApiParameter.QUERY, "Day of entry"),
    ("amount_min", OpenApiTypes.NUMBER, OpenApiParameter.QUERY, "Minimum amount"),
    ("amount_max", OpenApiTypes.NUMBER, OpenApiParameter.QUERY, "Maximum amount"),
    (
        "cat_title",
        OpenApiTypes.STR,
        OpenApiParameter.QUERY,
        "List of categories by name",
        True,
    ),
    (
        "cat_num",
        OpenApiTypes.INT,
        OpenApiParameter.QUERY,
        "List of categories by number",
        True,
    ),
)

common_query_parameters = [
    OpenApiParameter(**dict(zip(KWORDS, tuple_, strict=False)))  # type: ignore[arg-type]
    for tuple_ in param_tuples
]


def apply_query_filters(queryset, query_params):
    date_from = query_params.get("date_from")
    date_to = query_params.get("date_to")
    date_year = query_params.get("date_year")
    date_month = query_params.get("date_month")
    date_day = query_params.get("date_day")
    amount_min = query_params.get("amount_min")
    amount_max = query_params.get("amount_max")
    cat_title = query_params.getlist("cat_title")
    cat_num = query_params.getlist("cat_num")

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
                user=user, title="Starting Balance", amount=STARTING_BALANCE, category=None
            )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Stats(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=(
            common_query_parameters
            + [
                OpenApiParameter(
                    name="agg",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Aggregation functions, from django.db.models. Capitalized",
                    many=True,
                    enum=["Avg", "Count", "Max", "Min", "StDev", "Sum", "Variance"],
                )
            ]
        ),
        responses=StatsSerializer,
    )
    def get(self, request):
        expenses_queryset = Expense.objects.filter(user=request.user)
        expenses_queryset = apply_query_filters(expenses_queryset, self.request.query_params)
        incomes_queryset = Income.objects.filter(user=request.user)
        incomes_queryset = apply_query_filters(incomes_queryset, self.request.query_params)

        agg_functions = self.request.query_params.getlist("agg")
        if not agg_functions:
            return Response({"detail": "Please provide at least one 'agg' parameter."}, status=400)
        try:
            [getattr(django.db.models, agg) for agg in agg_functions]
        except Exception:
            return Response(
                {"detail": "Please provide 'agg' parameters supported by django.db.models."},
                status=400,
            )

        agg_params = {
            agg.lower(): getattr(django.db.models, agg)("amount") for agg in agg_functions
        }

        expenses_stats = expenses_queryset.aggregate(**agg_params)
        incomes_stats = incomes_queryset.aggregate(**agg_params)

        expenses_stats = {k: v or 0 for k, v in expenses_stats.items()}
        incomes_stats = {k: v or 0 for k, v in incomes_stats.items()}

        stats = {"expenses": expenses_stats, "incomes": incomes_stats}
        return Response(stats)


class CurrentBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=CurrentBalanceSerializer)
    def get(self, request):
        income_queryset = Income.objects.filter(user=request.user)
        total_income = income_queryset.aggregate(Sum("amount"))["amount__sum"] or 0
        expense_queryset = Expense.objects.filter(user=request.user)
        total_expense = expense_queryset.aggregate(Sum("amount"))["amount__sum"] or 0
        balance = {
            "total_income": total_income,
            "total_expense": total_expense,
            "current_balance": total_income - total_expense,
        }
        return Response(balance)
