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
from icu.view import qualityControl
from icu.view import englishStudy
from icu.view import wechat
from icu.view import notify
from icu.view import tools

urlpatterns = [
    # ApacheII评分表相关处理
    url(r'^tools/apacheII', include('icu.apacheII_urls')),
    url(r'^tools/apacheII/', include('icu.apacheII_urls')),

    # ICU工具集主页
    url(r'^$', tools.index),
    # 帮助
    url(r'^help$', tools.help),
    # ICU工具集相关
    url(r'^other_tools/(?P<keyword>\w*)$', tools.key),


    # 重症质控数据
    # 主页
    url(r'^qc$', qualityControl.index),

    # 编辑
    url(r'^qc/edit/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})$',
        qualityControl.edit),
    # 列表
    url(r'^qc/list/(?P<page>\d*)$', qualityControl.qcList),
    # 统计
    url(r'^qc/statistics$', qualityControl.statistics),
    # 下载质控评表
    url(r'^qc/download/(?P<condition>\w+)/(?P<parameter>\d*)$',
        qualityControl.download),
    # 质控报表(以年为参数进行报表)
    url(r'^qc/report/(?P<year>\d*)$', qualityControl.report),
    # 下载报表
    url(r'^qc/reportDownload/(?P<year>\d+)$', qualityControl.reportDownload),

    # 英语学习
    # 主页
    url(r'^englishStudy/$', englishStudy.index),
    # 编辑
    url(r'^englishStudy/edit/(?P<id>\d*)$', englishStudy.edit),
    # 查看
    url(r'^englishStudy/retrieve/(?P<id>\d+)$', englishStudy.retrieve),
    # 列表
    url(r'^englishStudy/list/(?P<page>\d*)$', englishStudy.list),


    # Wechat
    # server
    url(r'^wechat/', wechat.server),
    url(r'^miniPrograme/', wechat.miniPrograme),
    #url(r'^wechat/message/$', wechat.message),

    url(r'^$', qualityControl.index),

]
