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
from django.conf.urls import url
from django.contrib import admin
from notebook.view import note
from notebook.view import user
#我的实验室
from notebook.view import lab

urlpatterns = [

    #主页
    url(r'^$', lab.index),


    #相关操作存放于view.lab
    url(r'^lab$', lab.index),#实验室大厅主页面
    url(r'^mylab$', lab.mylab),#我的实验室主页面

    #编辑实验室数据
    url(r'^lab_edit/(?P<lab_id>\d*)$', lab.lab_edit),
    #编辑实验室中分组数据
    url(r'^group_edit/(?P<group_id>\d*)$', lab.group_edit),

    #数据逆向工程
    url(r'^reverse/(?P<lab_id>\d*)$', lab.reverse),

]
