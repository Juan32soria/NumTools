from django.urls import path
from . import views

urlpatterns = [
    path('', views.incrementalsearch_view, name='incremental_search'),
]
