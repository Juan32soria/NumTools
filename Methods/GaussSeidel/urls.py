from django.urls import path
from . import views

urlpatterns = [
  path('', views.gaussseidel_view, name='gaussseidel'),
]
