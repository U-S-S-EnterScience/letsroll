from django.urls import path
from . import views
from .views import ficha, home, cria_Ficha

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('ficha/', ficha, name='ficha'),
    path('cria_ficha/', cria_Ficha, name='cria_ficha'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]