"""
URL configuration for travel_guide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from currency_converter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('convert-currency/', views.CurrencyConversionView.as_view(), name='convert-currency'),
    path('get-safety-info/', views.SafetyInfoView.as_view(), name='get-safety-info'),
    path('get-country-codes/',views.Country_codeView.as_view(), name='get-country-codes'),
    path('get-safety-info/<str:country_code>/', views.SafetyInfoView.as_view(), name='get-safety-info'),
    path('emergency-services/', views.EmergencyServicesView.as_view(), name='emergency-services'),
    path('',include('user_operations.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)