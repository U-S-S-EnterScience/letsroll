from django.urls import path
from . import views
from .views import sheet, home

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('ficha/', sheet, name='ficha'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]