from django.urls import path
from . import views

urlpatterns = [
    path('', views.multipleroots_view, name='multipleroots'),
]
