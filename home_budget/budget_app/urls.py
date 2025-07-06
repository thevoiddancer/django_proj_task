from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, IncomeViewSet, CategoryViewSet, CurrentBalanceView, RegisterView, Stats
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('current_balance/', CurrentBalanceView.as_view()),
    path('stats/', Stats.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

