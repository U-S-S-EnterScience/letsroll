from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]