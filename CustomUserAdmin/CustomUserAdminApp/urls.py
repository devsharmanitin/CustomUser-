"""CustomUserAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from .views import *
from CustomUserAdminApp import views


urlpatterns = [
    
    
    path('account/user/register/' , views.UserAccountRegisterView , name='UserAccountRegisterView'),
    path('account/user/login/' ,views.UserAccountLoginView , name='UserAccountLoginView'),
    path('account/user/logout' , views.UserLogout , name='UserLogout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.ActivateEmail, name='activate'),  
    
    path('' , views.Dashboard , name='Dashboard'),
]
