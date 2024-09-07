"""
URL configuration for demostripe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from stripeapp. views import add_bank_account, bank_account_view,signup, verify_bank_account, verify_bank_account_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-bank-account/', add_bank_account, name='add_bank_account'),
    path('bank-account/', bank_account_view, name='bank_account_view'),
    path('verify-bank-account/', verify_bank_account_view, name='verify_bank_account_view'),
    path('verify-bank-account-action/',verify_bank_account, name='verify_bank_account'),
]