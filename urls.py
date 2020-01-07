"""pi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from notebook.view import note

urlpatterns = [
    url(r'^dhsadmin/', admin.site.urls),
    #下载数据库
    url(r'^test/$', note.data_test),
    #网络记事本app
    url(r'^notebook/', include('notebook.urls')),
    #ICU质控app
    url(r'^icu/', include('icu.urls')),
    #我的实验室
    url(r'^lab/', include('notebook.lab_urls')),
    #默认主页
    url(r'^$', note.index),
    ]

# 404页面
handler404 = note.page_not_found

