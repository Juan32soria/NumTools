from django.urls import path
from . import views

urlpatterns = [
    path('', views.partialpivot_view, name='partial_pivot'),
]
