from django.urls import path
from . import views
from .views import sheet, home, sheet_create
from django.contrib.auth import views as auth_views

app_name = 'pages'

urlpatterns = [
    #path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('', home, name='home'),
    path('sheet/<int:id>', sheet, name='sheet'),
    path('sheet_create/', sheet_create, name='sheet_create'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]