from django.urls import path
from . import views
from .views import sheet

app_name = 'pages'

urlpatterns = [
    path('', sheet, name='home'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]