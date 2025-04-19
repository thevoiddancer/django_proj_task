from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from upis.views import korisnik_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', korisnik_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='upis/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='upis/logout.html'), name='logout'),
    path('', include('upis.urls')),
]
