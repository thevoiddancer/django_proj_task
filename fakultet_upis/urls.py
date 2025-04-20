from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from upis.views import korisnik_login, register, korisnik_logout, user_admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', korisnik_login, name='login'),
    path('logout/', korisnik_logout, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='upis/logout.html'), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='upis/login.html'), name='login'),
    path('register/', register, name='register'),
    path('user_admin/', user_admin, name='admin'),
    path('', include('upis.urls')),
]

