from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, IncomeViewSet, CategoryViewSet, CurrentStateView, ExpenseByCategoryView, RegisterView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # path('', views.home, name='home'),
    path('', include(router.urls)),
    path('current_state/', CurrentStateView.as_view()),
    path('expense_by_category/', ExpenseByCategoryView.as_view()),
    path('register/', RegisterView.as_view()),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

