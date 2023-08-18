"""
URL configuration for leto project.

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
from zone_locker.views import zone_detail
from zone_locker.view.zone_list import ZoneListView, zone_lock, zone_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('zones/', ZoneListView.as_view(), name='zone_list'),
    path('', ZoneListView.as_view(), name='zone_list'),
    path('zone/<int:pk>/', zone_detail, name='zone_detail'),
    path('zone/<int:pk>/lock/', zone_lock, name='zone_lock'),
    path('zone/list/', zone_list, name='zone_lock'),


]
