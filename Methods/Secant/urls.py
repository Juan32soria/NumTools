from django.urls import path
from . import views

urlpatterns = [
    path('', views.secant_views, name='secant'),
]
