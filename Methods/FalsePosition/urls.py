from django.urls import path
from . import views

urlpatterns = [
  path('', views.false_position_view, name='false_position'),
]
