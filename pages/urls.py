from django.urls import path
from . import views
from .views import sheet, home, sheet_create

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('sheet/<int:id>', sheet, name='sheet'),
    path('sheet_create/', sheet_create, name='sheet_create'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]