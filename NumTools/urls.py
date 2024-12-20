"""
URL configuration for NumTools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('bisection/', include('Methods.Bisection.urls')),
    path('false_position/', include('Methods.FalsePosition.urls')),
    path('fixed_point/', include('Methods.FixedPoint.urls')),
    path('incremental_search/', include('Methods.IncrementalSearch.urls')),
    path('secant/', include('Methods.Secant.urls')),
    path('newton/', include('Methods.Newton.urls')),
    path('multipleroots/', include('Methods.MultipleRoots.urls')),
    path('jacobi/', include('Methods.Jacobi.urls')),
    path('simplegauss/', include('Methods.SimpleGauss.urls')),
    path('gaussseidel/', include('Methods.GaussSeidel.urls')),
    path('lu/', include('Methods.LU.urls')),
    path('cholesky/', include('Methods.Cholesky.urls')),
    path('gpartialpivot/', include('Methods.GPartialPivot.urls')),
]
