from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='upis-home'),
    path('', views.SmjeroviListView.as_view(), name='upis-home'),
    path('prijava/', views.prijava_view, name='prijava'),
    path('prijava/<str:smjer>', views.prijava_view, name='prijava'),
    path('admin/', admin.site.urls),
    path('login/', views.korisnik_login, name='login'),
    path('logout/', views.korisnik_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_admin/', views.user_admin, name='admin'),
    path('<str:smjer>/', views.PredmetiListView.as_view(), name='predmeti_list'),
]
