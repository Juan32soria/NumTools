from django.urls import path
from . import views

urlpatterns = [
    path('', views.newton_view, name='newton'),
]
