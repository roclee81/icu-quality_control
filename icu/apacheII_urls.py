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
from icu.view import apacheII

urlpatterns = [
    #首页
    url(r'^$', apacheII.index),
    #增加一个ApacheII评分表
    url(r'^add$', apacheII.add),
    #下载ApacheII评分表
    url(r'^download/(?P<condition>\w+)/(?P<parameter>\d*)$', apacheII.download),
    #url(r'^download/(month)/(?P<month>\d*)$', apacheII.download),
    #url(r'^download/(id)/(?P<id>\d+)$', apacheII.download),
    #修改一个存在的ApacheII评分表
    url(r'^update/(?P<id>\d+)$', apacheII.update),
    #查看一个ApacheII评分表
    url(r'^retrieve/(?P<id>\d+)$', apacheII.retrieve),
    #查看列表
    url(r'^list/(?P<page>\d*)$', apacheII.apacheIIList),
    #统计数据
    url(r'^statistics$', apacheII.statistics),
    ]


