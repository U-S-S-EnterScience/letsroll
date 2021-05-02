from django.urls import path
from . import views
from .views import ficha, home

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('ficha/', ficha, name='ficha'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]