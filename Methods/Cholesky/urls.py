from django.urls import path
from . import views

urlpatterns = [
    path('', views.cholesky_view, name='cholesky'),
]
