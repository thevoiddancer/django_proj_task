from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CurrentBalanceView,
    ExpenseViewSet,
    IncomeViewSet,
    RegisterView,
    Stats,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"incomes", IncomeViewSet, basename="income")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
    path("register", RegisterView.as_view()),
    path("token", obtain_auth_token, name="api_token_auth"),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema")),
    path("current_balance", CurrentBalanceView.as_view()),
    path("stats", Stats.as_view()),
]
