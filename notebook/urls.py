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

    #初始化数据库，增加默认用户名
    url(r'^init/$', note.init),
    #主页
    url(r'^$', note.index),
    #favicon
    url(r'^favicon.ico$', note.favicon),


    #相关操作存放于view.user
    url(r'^verify.jpg$', user.verifyimg),#用户注册页面
    url(r'^user/reg$', user.reg),#用户注册页面
    url(r'^user/login$', user.user_login),#用户登录页面
    url(r'^user/logout$', user.logout),#退出登录页面
    url(r'^user/info$', user.info),#用户信息页面
    url(r'^user/update_info$', user.update_info),#用户信息页面
    #url(r'^notebook/user/send_verify_email$', user.send_verify_email),#发送邮箱验证邮件
    #url(r'^notebook/user/email_verify/(.+)/(.+)$', user.email_verify),#邮箱验证页面

    url(r'^note/search/(?P<topic>\w*)/(?P<keyword>\w*)$', note.search), #搜索笔记
    url(r'^note/retrieve/(?P<id>\d+)$', note.retrieve), #浏览笔记
    #url(r'^notebook/note/left$', note.note_left), #查询left
    url(r'^note/list/(?P<basedir_id>\d*)$', note.tree_list), #查询列表
    url(r'^note/list/show_deleted/$', note.tree_list,{'deleted':1}), #查询已删除笔记
    url(r'^form/note/create/(?P<basedir_id>\d+)/(?P<note_type>\d)$', note.form_create), #创建笔记表单
    url(r'^note/create/$', note.create),#创建笔记表单
    url(r'^form/note/update/(?P<id>\d+)$', note.form_update), #更新笔记表单
    url(r'^note/update/$', note.update), #更新笔记
    url(r'^note/remove/(?P<id>\d+)$', note.remove), #删除笔记到回收站
    url(r'^note/empty_recycle_bin/$', note.empty_recycle_bin), #清空回收站
    url(r'^note/change_dir/(?P<id>\w+)/(?P<basedir_id>\w+)$', note.change_dir), #更改笔记路径
    url(r'^help$', note.help),#知识库帮助信息


]
