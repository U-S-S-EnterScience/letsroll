from django.urls import path
from . import views
from .views import home

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]