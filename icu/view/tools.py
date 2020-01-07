#!/usr/bin/python3
from django.shortcuts import render, render_to_response
from django.http import HttpResponse as HR
from django.http import HttpResponseRedirect
from notebook.models import User

from settings import BASE_DIR
import os
import base64
import random
import datetime
import functools


# 用户登录装饰器
def login(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        # 将request传入包装器内，以便查询用户登录session
        request = args[0]
        # 如果没有登录，跳转到登录页面
        if not request.session.get('uid', 0):
            request.session['referrerUrl'] = request.path
            return HttpResponseRedirect("/notebook/user/login")
        # 提取登录的用户信息
        user = User.objects.get(id=request.session['uid'])
        # 如果已经登录，执行请求的函数
        # 将登录用户信息 user作为参数添加进去
        return func(*args, **kw, user=user)
    return wrapper


# 设置主页及一些静态内容模板的返回

# ICU工具集主页，
@login
def index(request, user):
    # 默认主页为index
    template = "icu/index.html"
    return render(request, template, {'user': user})


# ICU工具集帮助文件
@login
def help(request, user):
    template = "icu/help.html"
    return render(request, template, {'user': user})

# ICU工具集，不同的keyword返回不同的工具集模板，
@login
def key(request, keyword, user):
    if not keyword:
        keyword = 'others_list'
    template = "icu/tools/" + keyword + ".html"
    return render(request, template, {'user': user})
