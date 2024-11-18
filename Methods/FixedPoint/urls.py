from django.urls import path
from . import views

urlpatterns = [
  path('', views.fixed_point_view, name='fixed_point'),
]
