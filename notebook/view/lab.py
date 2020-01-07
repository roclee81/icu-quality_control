#!/usr/bin/python3
'''
我的实验室
从目前国家的政策走向来看，一切都在走向正规化，违法的成本越来越高，违法被抓住的几率越来越高
因此，无论做什么事情，守法才是王道。
对于论文写作，全中国医学论文都是在造假，大致院士，小至小医生。
有的靠买，有的靠骗，可谓乌烟瘴气。
这一切都会随着国家政策的收紧而出现变化。
我的实验室是这样一个在线网站：
1、提供创建我的实验室，记录实验数据
2、提供实时的数据统计功能
3、提供数据假设检验功能
4、对于一些统计小白，提供数据逆向功能
    4.1、可以根据结果，倒推数据,做出模拟数据出来(收费？)
5、我的实验室，像极了gitHub   

'''
from django.shortcuts import render,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse as HR
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count,Sum, Avg, Max, Min

from notebook.models import User

from pyecharts import Bar, Line
from pyecharts.engine import create_default_environment

import time
import datetime
import html2text
import functools

#模板文件路径
templateBase = "stats/"

#用户登录装饰器
def login(func):
    @functools.wraps(func)
    def wrapper(*args,**kw):
        #将request传入包装器内，以便查询用户登录session
        request = args[0]
        #如果没有登录，跳转到登录页面
        if not request.session.get('uid',0):
            request.session['referrerUrl'] = request.path
            return HttpResponseRedirect("/notebook/user/login")
        #提取登录的用户信息
        user=User.objects.get(id=request.session['uid'])
        #如果已经登录，执行请求的函数
        #将登录用户信息 user作为参数添加进去
        return func(*args,**kw,user=user)
    return wrapper

'''
主页
显示实验室大厅
在实验室大厅中，所有实验者的实验室数据被展示
显示分导航栏：我的实验室、登录等等……
'''
def index(request):
    #定义一个空的用户
    user = {}
    #查看当前是否有用户登录
    if request.session.get('uid',0):
        #提取登录的用户信息
        user=User.objects.get(id=request.session['uid'])
    #加载首页模板
    template = templateBase + "index.html"
    return render(request,template,{'user':user})

'''
我的实验室
在我的实验室中，显示专属于我的实验室数据
显示我可以操作的部分
'''
@login
def mylab(request,user):
    template = templateBase + "mylab.html"
    return render(request,template,{'user':user})

#编辑我的实验室
@login
def lab_edit(request,lab_id,user):
    # GET时显示表单
    if request.method == 'GET':
        #显示表单
        template = templateBase + "form_lab.html"
        return render(request,template,{'user':user})
    #如果POST数据，处理提交的数据
    elif request.method =='POST':
        #qc保存提交的质控数据
        qc = {}
        #整理数据，保存在qc 中
        cleanUp(request,qc)
        #验证数据有效性
        errors = validate(request,qc,action)
        if errors:
            pass
        #存储
        storeQc = store(request,user,qc,action)
        template = "icu/tools/qualityControl/submitSuccess.html"
        return render(request,template,{'qc':storeQc})



#整理用户提交的数据，使用字典参数qc保存数据
def cleanUp(request,qc):
    pass

#审核用户提交的数据，确认数据，以保存复数准确
def validate(request,qc,action):
    errors =[]
    return errors


#存储用户数据和最终结果
def store(request,user,qc,action):
    #新建数据库数据
    if action == 'create':
        pass

    #更新数据
    elif action == 'update':
        pass



#编辑我的实验小组
@login
def group_edit(request,group_id,user):
    template = templateBase + "form_group.html"
    return render(request,template,{'qc':storeQc})


#实验室逆向数据
@login
def reverse(request,lab_id,user):
    template = templateBase + "reverse.html"
    return render(request,template,{'user':user})

