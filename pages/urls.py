from django.urls import path
from . import views
from .views import ficha, home, cria_Ficha
from django.contrib.auth import views as auth_views

app_name = 'pages'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('home/', home, name='home'),
    path('ficha/<int:id>', ficha, name='ficha'),
    path('cria_ficha/', cria_Ficha, name='cria_ficha'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]