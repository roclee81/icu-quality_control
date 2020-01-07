#!/usr/bin/python3
from django.shortcuts import render,render_to_response
from django.http import HttpResponse as HR
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.db.models import Q,Count

from settings import BASE_DIR
from notebook.models import User,Note,Log,Fortune
import os
import re
import random
import time
import functools
import requests

#用户行为日志装饰器
def log(func):
    @functools.wraps(func)
    def wrapper(request, *args,**kw):
        user = request.session['user'] #为登录后日志
        url = request.path
        agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']
        #将用户的用户名，访问url，浏览器标识，ip记录入数据库
        log = Log.objects.create(user=user,url=url,agent=agent,ip=ip)
        #print(user,url,agent,ip)
        #print("这是用户日志",request.path)
        return func(request, *args,**kw)
    return wrapper

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

@login
def index_jump(request,user):
    return HttpResponseRedirect("/notebook/")

# help信息
def help(request):
    #显示note主体内容
    return render(request,'help.html')

# 404页面
def page_not_found(request,exception):
    #显示note主体内容
    return render(request,'404.html')   

@login
def index(request,user):
    #显示note主体内容
    notes=Note.objects.filter(user=user,basedir_id=0,deleted=0).order_by('note_type')
    #统计 dir 和 file的数量
    r = Note.objects.filter(user=user,deleted=0).values("note_type").annotate(count=Count('id')).order_by()

    #保存统计结果到的目录和文件数量
    count = {'dir':0,'file':0}
    #如果没有返回值，不应报错
    try:
        count['dir'] = r.filter(note_type=0).values('count')[0]['count']
    except:
        pass
    try:
        count['file'] = r.filter(note_type=1).values('count')[0]['count']
    except:
        pass

    #每日一句api
    #sentence = requests.get("http://open.iciba.com/dsapi/").json()
    id = random.randint(1,30014)
    sentence = Fortune.objects.get(id=id).content
    sentence = re.sub("\n","<P>",sentence)
    sentence = re.sub(r"\x1b\x5b\d+m","&nbsp;&nbsp",sentence)
    sentence = re.sub(r"\x1b\x5bm","",sentence)

    return render(request,'index.html',{'count':count, 'notes':notes, 'user':user, 'basedir_id':0, 'sentence':sentence})

def favicon(request):
    image_data = open("static/favicon.ico","rb").read()   
    return HR(image_data,content_type="image/ico")

#下载数据库功能
def data_test(request):
    #先登录
    #if not request.session.get('uid',0):
        #request.session['referrerUrl'] = request.path
        #return HttpResponseRedirect("/notebook/user/login")

    #user=User.objects.get(id=request.session['uid'])
    #非管理员，直接返回，不允许执行命令
    #if user.name != 'dhs':
        #return HR('user:%s you win !'%user.name)

    tempPath = os.path.join(BASE_DIR,"static/temp/")
    cmdFile = "cmd"

    from subprocess import Popen
    #重启电脑命令
    if request.GET.get('cmd','0') == 'reboot':
        Popen('shutdown -r -t 0',shell=True)
        return HR('cmd reboot OK')
    #重启Apache服务器
    elif request.GET.get('cmd','0') == 'restartServer':
        #Apache mod_wsgi目前不能执行进程程序，只能曲线救国，写入本地cmd文件
        #让本地执行
        with open(tempPath+cmdFile,'w') as fd:
            fd.write('restartServer')
        return HR('cmd restartServer OK')
    # git Pull
    elif request.GET.get('cmd','0') == 'gitPull':
        #Apache mod_wsgi目前不能执行进程程序，只能曲线救国，写入本地cmd文件
        #让本地执行
        with open(tempPath+cmdFile,'w') as fd:
            fd.write('gitPull')
        return HR('cmd gitPull OK')
    # migrate
    elif request.GET.get('cmd','0') == 'migrate':
        Popen('python manage.py migrate',shell=True)
        return HR('cmd migrate OK')
    # grab
    elif request.GET.get('cmd','0') == 'grab':
        #from PIL import ImageGrab,Image
        #img = ImageGrab.grab()        #实现截屏功能
        #w,h =img.size
        #img =img.resize((int(w/2),int(h/2)),Image.ANTIALIAS)
        #img.save('static/temp/grab.png','PNG') #设置保存路径和图片格式

        #Apache mod_wsgi目前不能执行进程程序，只能曲线救国，写入本地cmd文件
        #让本地执行
        with open(tempPath+cmdFile,'w') as fd:
            fd.write('grab')
        return HR('<img src="/static/temp/grab.png?%s">'%str(time.time()))



    #下载数据库
    elif request.GET.get('cmd','0') == 'dhsdjango':
        def file_iterator(file_name, chunk_size=512):
            with open(os.path.join(BASE_DIR,file_name),"rb") as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        the_file_name = "django-addon.exe"
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response
    else:
        return HR('data_test ok')



#初始化数据库，增加一个用户，以免新建代码仓库查询时出现无用户错误
def init(request,name='test'): 
    try:
        user=User.objects.create(name=name)
    except:
        user=User.objects.get(name=name)

    #增加回收站文件夹，type类型10
    note_recycle = Note.objects.create(
            user = user, 
            note_type=10,#回收站note_type=10
            title = "回收站",
            basedir_id = 0) 

    note=Note.objects.create(
            user = user, 
            title = "操作指南",
            content = "<p>我是一个文件夹,文件夹是种特殊的笔记，因为它不仅可以当作日记，也可以被当作分类目录，在里面存放日记</p>",
            basedir_id = 0) 

    note2=Note.objects.create(
            user = user, 
            title = "创建笔记",
            content = "<p>要想创建新的笔记或者分类很简单，试试点击灰色的文件夹或者文件图标就可以了!</p>",
            basedir_id = note.id,
            note_type=1)

    note3=Note.objects.create(
            user = user, 
            title = "修改笔记",
            content = "<p>这是我的第一条日记，试试修改看看，也可以拖拽我到更合适的分类去!</p>",
            basedir_id = note.id,
            note_type=1)

    note4=Note.objects.create(
            user = user, 
            title = "删除笔记",
            content = "<p>警告：删除分类很危险，您将删除分类下面所有的笔记!<br>需要慎重操作！！！</p>",
            basedir_id = note.id,
            note_type=1)

    note0=Note.objects.create(
            user = user, 
            title = "欢迎使用网络记事本",
            content = "<p>抛开复杂，让它帮我们记住更多锁事。提醒功能在开发中……</p>",
            basedir_id = 0,
            note_type=1)
    return 


#根据id，返回笔记内容

@login
@log #登录后才记录日志
def retrieve(request,id,user):
    note=Note.objects.get(id=id,user=user)

    #定义函数getBase获取 note 的父目录的名称
    #直接将父目录的名称存储到basedirs列表中
    #返回：父目录的父目录id
    def getBase(baseId,basedirs):
        #设置返回条件:如果到达顶目录id，返回
        if baseId == 0:
            return
        basedir = Note.objects.get(id=baseId,user=user)
        basedirs.insert(0,basedir.title)
        #递归调用getBase
        getBase(basedir.basedir_id,basedirs)

    #使用basedirs 列表存储该项笔记的所有父目录名称
    basedirs=[]
    getBase(note.basedir_id,basedirs)

    #print(basedirs)
    return render(request,'note_retrieve.html',{'note':note,'basedirs':basedirs})

#表单/增加一条笔记，参数为basedir_id(父目录的id)
@login
def form_create(request,basedir_id,note_type,user):
    basedir={'title':'根目录','id':0}
    basedir_id=int(basedir_id)
    if basedir_id != 0:
        basedir=Note.objects.get(id=basedir_id)
    return render(request,'form_note_create.html',{'basedir':basedir,'note_type':note_type})

#表单/修改一条笔记，参数为id(知识点的id)
@login
def form_update(request,id,user):
    note=Note.objects.get(id=id,user=user)
    return render(request,'form_note_update.html',{'note':note})

#创建一条笔记，参数为basedir_id(父目录的id)
@login
def create(request,user):

    basedir_id = int(request.POST['basedir_id'])
    note_type = int(request.POST['note_type'])

    note=Note.objects.create(user=user,
        title=request.POST['title'],
        content=request.POST['content'],
        basedir_id = basedir_id,
        note_type=note_type)
    return render(request,'add_to_list.html',{'note':note,'basedir_id':basedir_id})

#更改路径
@login
def change_dir(request,id,basedir_id,user):
    id=int(id[3:])

    noteToChange = Note.objects.get(id=id,user=user)

    #将文件作为父目录的操作
    if (basedir_id.startswith("title_")):
        #先查看此父目录是不是合法的目录
        baseNote=Note.objects.get(id=int(basedir_id[6:]),user=user)
        if (baseNote.note_type==0 or baseNote.note_type == 10):
            basedir_id=int(basedir_id[6:])
        else:
            basedir_id=baseNote.basedir_id
    #拟更改到文件夹下面的操作
    elif(basedir_id.startswith("div_")):
        #先查看此父目录是不是合法的目录
        baseNote=Note.objects.get(id=int(basedir_id[4:]),user=user)
        #如果拟移动到的父目录是一个目录
        if (baseNote.note_type == 0 or baseNote.note_type == 10):
            basedir_id=int(basedir_id[4:])
        else:
        #如果拟移动到的父目录并不是一个目录，则取它的上一级目录,实际操作并无此结果出现
            basedir_id=baseNote.basedir_id
    #拟更改到ul开头的目录的操作
    elif(basedir_id.startswith("ul_")):
        basedir_id=int(basedir_id[3:])
    else:
        return render(request,'note_info.html',{'noteInfo':'不允许移动到此目录!!'})


    #回收站不允许更改到其它目录
    if noteToChange.note_type == 10:
        return render(request,'note_info.html',{'noteInfo':'回收站不能更改到其它目录!'})

    noteToChange.basedir_id = basedir_id
    noteToChange.save()

    return render(request,'note_info.html',{'noteInfo':'文件目录已经更改'})

#修改笔记
@login
def update(request,user):
    id=int(request.POST['id'])
    Note.objects.filter(id=id,user=user).update(
            title=request.POST['title'],
            content=request.POST['content'])

    #notes=Note.objects.filter(basedir=None,user=user)
    return HR(request.POST['title'][0:10])

#搜索笔记，返回列表
@login
def search(request, topic, keyword, user):
    '''
    搜索笔记功能有两个关键字组成，
    一个是topic[title,all]表示搜索的主题是仅标题，还是全文搜索
    另一个是keyword关键字，表示要搜索的内容
    如果没有keyword，表示返回所有列表，不需要搜索
    '''
    if keyword:
        #如果搜索主题 topic为仅标题
        if topic == 'title':
            notes=Note.objects.filter(Q(user=user) & Q(deleted=0) & Q(title__icontains=keyword) ).order_by('note_type')
        #如果搜索主题 topic为仅全文
        elif topic == 'all':
            notes=Note.objects.filter(Q(user=user) & Q(deleted=0) & (Q(title__icontains=keyword)|Q(content__icontains=keyword))).order_by('note_type')
            
    else:
        #直接返回全部list
        return tree_list(request)
    return render(request,'list.html',{'notes':notes,})

#仅返回list部分
@login
def tree_list(request,user,basedir_id=0,deleted=0):
    notes=Note.objects.filter(user=user,basedir_id=basedir_id,deleted=deleted).order_by('note_type')
    return render(request,'list.html',{'notes':notes,})



#移到回收站，参数为笔记id
#实际是修改上级目录为回收站，与电脑相似
@login
def remove(request,id,user):
    note_recycle = Note.objects.get(note_type = 10,user=user)
    Note.objects.filter(id=id,user=user).update(basedir_id = note_recycle.id)

    return render(request,'note_info.html',{'noteInfo':'笔记已经被删除'})



#清空回收站
@login
def empty_recycle_bin(request,user):

    def sign_all(basedir,user):
        '''
        sign_all 函数用来删除某个文件夹下面所有的文件
        其实是增加了delete 删除标记为 1，并没有真正删除，
        为以后数据找回留下余地
        在遇到文件夹时，递归调用本函数
        '''
        #获取此目录下需要标记为删除的文件
        notesToDelete = Note.objects.filter(basedir_id=basedir.id, deleted=0, user=user)
        #notesToDelete = Note.objects.filter(basedir_id=basedir.id,  user=user)

        #遍历文件，执行删除标记
        #notesToDelete.update(deleted=1)
        #不能这样执行删除标记，如果执行了，queryset就会因为不满足deleted = 0而被清空，
        #后续工作不能进行
        #这是一个坑！
        for note in notesToDelete:
            note.deleted = 1
            note.save()
            #如果要删除的文件为文件夹，递归执行删除文件夹下面的文件
            if note.note_type == 0:
                sign_all(note,user)

    #以回收站为根目录，开始调用函数
    note_recycle = Note.objects.get(note_type=10, user=user)
    sign_all(note_recycle,user)


    return render(request,'note_info.html',{'noteInfo':'回收站已清空！！！'})


