from django.urls import path
from . import views

urlpatterns = [
    path('', views.lu_view, name='lu'),
]
