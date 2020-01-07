from django.shortcuts import render,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse as HR
from django.http import HttpResponseRedirect
from django.http import JsonResponse



from notebook.models import User
from icu.models import Bilingual
from icu.models import Bilingual

from icu.view import translate  #逐句翻译为translate.sbs  整段翻译为translate.para

import time
import datetime
import functools

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

# 英语学习主页
@login
def index(request,user):

    return HttpResponseRedirect("/icu/englishStudy/list")

    template = "icu/tools/englishStudy/index.html"
    return render(request,template,{'user':user})


#编辑英语学习语料
@login
def edit(request,id,user):

    workmates = user.workmate.split(",")

    #bil保存提交的语料
    bil = {}

    # GET时显示表单
    if request.method == 'GET':
        src =''
        #如果编辑已经存在的id时
        if id:
            bils = Bilingual.objects.filter(user=user,id=id)
            if bils:
                bil = bils[0]
        #显示表单
        template = "icu/tools/englishStudy/edit_form.html"
        return render(request,template,{'user':user,'bil':bil,'workmates':workmates})

    #如果POST数据，处理提交的数据
    elif request.method =='POST':
        #整理数据，保存在bil 中
        cleanUp(request,bil)

        bils = Bilingual.objects.filter(user=user,id=bil['id'])
        if bils:
            #若已经存在此id数据，则update
            action = "update"
        else:
            #若没有数据，则 create
            action = "create"
            
        #确认提交数据
        errors = validate(request,bil,action)
        if errors:
            template = "icu/tools/englishStudy/submitError.html"
            return render(request,template,{'errors':errors,})
        #存储
        storeBil = store(request,user,bil,action)
        template = "icu/tools/englishStudy/submitSuccess.html"
        return render(request,template,{'user':user,'bil':storeBil})

#查看
@login
def retrieve(request,id,user):
    bil=Bilingual.objects.get(user=user,id=id)

    template = "icu/tools/englishStudy/retrieve.html"
    return render(request,template,{'user':user,'bil':bil})

#整理用户提交的数据，使用字典参数bil保存数据
def cleanUp(request,bil):
    bil['id'] = request.POST.get('id',0)
    bil['src'] = request.POST.get('src','')
    bil['ip'] = request.META.get('REMOTE_ADDR','') #IP地址
    bil['doctor'] = request.POST.get('doctor','')
    bil['length'] = len(bil['src'])



#审核用户提交的数据，确认数据，以保存复数准确
def validate(request,bil,action):
    errors =[]
    if bil['length'] > 2000:
        errors.append('目前翻译流量限制，不翻译超过2000字符的文档！')
        return errors

    #通过翻译器翻译数据
    bil['dst'] = translate.para(bil['src'])[1]
    bilList = translate.sbs(bil['src'])
    bil['bil']=''
    for b in bilList:
        bil['bil'] += "原文:%s\n译文:%s\n"%(b[0],b[1])

    return errors

#存储用户数据和最终结果
def store(request,user,bil,action):
    #新建数据库数据
    if action == 'create':
        storeBil = Bilingual.objects.create(
                user = user,
                #质控信息
                src = bil['src'],
                length = bil['length'],
                dst = bil['dst'],
                bil = bil['bil'],
                doctor = bil['doctor'],
                ip = bil['ip'],
                             )
    #更新数据
    elif action == 'update':
        # up 表示update patient
        storeBil = Bilingual.objects.get(id=bil['id'],user=user)
        storeBil.src = bil['src']
        storeBil.length = bil['length']
        storeBil.dst = bil['dst']
        storeBil.bil = bil['bil']
        storeBil.doctor = bil['doctor']
        storeBil.ip = bil['ip']
        storeBil.save()
    return storeBil
            





#Bilingual列表 list
@login
def list(request,page,user):

    #每次显示20个数据
    count =20

    bils_all = Bilingual.objects.filter(user=user)

    paginator = Paginator(bils_all,count)

    try:
        bils = paginator.page(page) # bils为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bils = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        bils = paginator.page(paginator.num_pages)

    #页面范围
    page_range =paginator.page_range
    #计数器开始值,使用负值，以便在模板中可以使用加法tag
    start = (bils.number-1) * count  - bils_all.count() - 1 


    template = "icu/tools/englishStudy/list.html"
    return render(request,template,{'user':user,'bils':bils,'page_range':page_range,'start':start})

