"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('terms/', views.terms),
    path('',views.post_list_view,name='home'),
    path('createpost/',views.create),
    path('showpost/',views.showpost.as_view(),name="showpost"),
    path('tag/<str:tag_slug>/',views.post_list_view,name='post_list_tag_by_name'),
    path('complete/<int:year>/<int:month>/<int:date>/<str:post>',views.detail_view,name='post_detail'),
    path('share/<int:id>/',views.sharmebymail),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
    path('about/',views.about),
]
