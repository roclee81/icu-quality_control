#!/usr/bin/python3
from django.shortcuts import render, render_to_response
from django.http import HttpResponse as HR
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
# 启用@csrf_protect装饰器保护某些函数
from django.views.decorators.csrf import csrf_exempt, csrf_protect


from settings import BASE_DIR
from notebook.models import User, Note
from notebook.view import note
import os
import re
# import random
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


# 生成验证码图片
def verifyimg(request):
    from notebook.verify import genImg
    imgbuf, verify_code = genImg()
    request.session['verify_code'] = verify_code
    return HR(imgbuf.getvalue(), 'image/gif')


@csrf_protect
# 用户登录
# 为避免与 原本网页的 login 函数冲突，使用了user_login
def user_login(request):
     # 如果GET则显示login_form页面
    if request.method == 'GET':
        # 如果用户已经登录
        if request.session.get('uid', 0):
            return HttpResponseRedirect("/notebook/")

        if not request.session.get('referrerUrl', ''):
            request.session['referrerUrl'] = request.META.get(
                'HTTP_REFERER', '')

        request.session.setdefault('try_times', 0)
        return render(request, 'login_form.html')
     # 如果POST数据，则处理数据
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST.get('verify', None)
        verify_code = request.session.get('verify_code', None)

        request.session.setdefault('try_times', 0)
        request.session['try_times'] += 1
        request.session['verify_code'] = None  # 使验证码缓存失效

        error = []

        # 如果使用test帐号，直接不用验证密码登录
        if username == "test":
            user = User.objects.filter(name=username)
        else:
            # 如果验证码错误，直接返回
            if (verify_code is not None) and (
                    verify_code.lower() != verify.lower()):
                error.append(u'验证码输入错误')
                return render(request, 'login_form.html', {'error': error, })

            user = User.objects.filter(name=username, passwd=password)

         # 验证用户名及密码
        if user.count() < 1:
            error.append(u'用户名或密码错误')
         # 输入出错，返回登录页面，提示出错信息
        if error:
            return render(request, 'login_form.html', {'error': error, })

        # 设置session
        if request.POST.get('remember_me', None):
            request.session.set_expiry(3600 * 24 * 7)
        else:
            request.session.set_expiry(0)

        request.session['try_times'] = 0
        request.session['user'] = user[0].name
        request.session['uid'] = user[0].id
        return render(
            request, 'login_success.html', {
                'referrerUrl': request.session['referrerUrl']})


# 退出登录
def logout(request):
     # 清空session
    request.session.flush()

    return HttpResponseRedirect("/notebook/user/login")


# 用户注册
def reg(request):
     # 如果GET则显示reg_from页面
    if request.method == 'GET':
        return render(request, 'reg_form.html')
     # 如果POST数据，则处理数据
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        error = []
        # 如果用户名长度不正确
        if not 1 <= len(username):
            error.append(u'至少得有一个用户名！')
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_]{0,15}$', username):
            error.append(u'用户名不规范')

         # 如果用户名已经存在
        if User.objects.filter(name=username).count() != 0:
            error.append(u'用户名已经存在')

         # 输入出错，返回注册页面，提示出错信息
        if error:
            reginfo = {'username': username, }
            return render(
                request, 'reg_form.html', {
                    'error': error, 'reginfo': reginfo})

        user = User(name=username, passwd=password,)
        user.save()
        note.init(request, username)

        # 注册成功,设置session
        request.session['user'] = username
        request.session['uid'] = user.id

        return render(request, 'reg_success.html', {'user': request.session})


# 发送邮件以验证邮箱
@login
def send_verify_email(request, user):
    email_verify_code = user.email_verify_code
    if email_verify_code == 'success':
        return
    username = user.username
    email = user.email
    addenMsg = request.POST['msg']

    # 如果增加内容过少
    if len(addenMsg) < 100:
        pass

    email_verify_url = r'http://127.0.0.1:8000/email_verify/%s/%s' % (
        username, email_verify_code)
    emailmsg = u'尊敬的朋友，如果您在主治医师研讨班注册了帐号，请点击以下网址完成邮箱认证\n\
                %s  \n如果没有注册，请忽略此邮件，谢谢！\n\n\n' % (email_verify_url)
    # 加上用户的乱码，这样就可以了 ,夹心饼
    emailmsg = addenMsg + emailmsg + addenMsg

   # 发送 email 认证  Email认证后，用户的degree 增加 1 ，也就可以发讨论信息了
    from doctor.settings import EMAIL_HOST_USER
    from django.core.mail import send_mail
    # send_mail(u'用户邮箱认证DjangoMail',emailmsg,EMAIL_HOST_USER,[email],fail_silently=False)
    send_mail(
        u'用户邮箱认证DjangoMail',
        emailmsg,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False)
    return HttpResponseRedirect("/notebook/user/login")


# 用户Email邮箱验证
def email_verify(request, username, email_verify_code):
    # 删除末尾的空格，只保留字符
    email_verify_code = re.match(r'(\w+)', email_verify_code).group(0)

    if User.objects.filter(username=username,
                           email_verify_code='success').count() == 1:
        return HR(u'您已经邮箱认证成功，请忽反复认证！')

    user = User.objects.filter(
        username=username,
        email_verify_code=email_verify_code)
    if user.count() == 1:
        u = user[0]
        u.email_verify_code = 'success'
        u.degree += 1
        request.session['degree'] = u.degree
        u.save()
        return HR(u'认证成功')
    else:
        return HR(u'认证失败,请重新注册')


# 用户信息显示页
@login
def info(request, user):

    return render(request, 'user_info.html', {'user': user})

# 用户信息修改页
@login
@csrf_protect
def update_info(request, user):

    # 如果GET则显示表单页面
    if request.method == 'GET':
        return render(request, 'form_userinfo.html', {'user': user})
    # 如果POST数据
    elif request.method == 'POST':
        # e用来保存出错信息
        error = []
        # 使用参数变量来动态调整 update的数据
        parameter = {}

        # 用户密码验证
        passwd = request.POST['password']
        new_passwd = request.POST['new_password']
        new_passwd2 = request.POST['new_password2']

        # 若验证密码不正确，拒绝修改用户信息
        if passwd != user.passwd:
            error.append('您的登录验证密码有误，不能修改信息！')
        # 在验证密码正确情况下，若填写了新密码
        elif (new_passwd or new_passwd2):
            # 如果两个新密码不一致
            if (new_passwd != new_passwd2):
                error.append('两次输入的新密码不一致!')
            else:
                # 设置新密码为当前密码
                passwd = new_passwd

        # 如果选择了删除部门照片
        if request.POST.get('removeDepartmentImg', 0):
            parameter['departmentImg'] = ''
            try:
                # 删除原来的文件
                os.remove(
                    os.path.join(
                        BASE_DIR,
                        'static/images/department/',
                        user.departmentImg))
            except BaseException:
                pass
        # 如果提交了部门照片信息
        elif request.FILES.get('departmentImg', 0):
            f = request.FILES['departmentImg']
            # 如果文件不大于200K
            if f.size < 200000:
                ext = os.path.splitext(f.name)[1]
                departmentImg = user.name + ext

                try:
                    # 删除原来的文件
                    os.remove(
                        os.path.join(
                            BASE_DIR,
                            'static/images/department/',
                            user.departmentImg))
                except BaseException:
                    pass

                try:
                    # 建立新文件
                    with open(os.path.join(BASE_DIR, 'static/images/department/', departmentImg), 'wb+') as imgStore:
                        for chunk in f.chunks():
                            imgStore.write(chunk)
                    # 设置新的文件名
                    parameter['departmentImg'] = departmentImg
                except BaseException:
                    pass
            else:
                error.append('上传的图片文件不能大于200KB !')

        # 如果有出错信息，返回表单重填
        if error:
            return render(
                request, 'form_userinfo.html', {
                    'error': error, 'user': user})
        else:
            parameter['passwd'] = passwd
            parameter['email'] = request.POST['email'] or None
            parameter['qq'] = request.POST['qq'] or None
            parameter['phone'] = request.POST['phone'] or None
            parameter['company'] = request.POST['company'] or None
            parameter['department'] = request.POST['department'] or None
            # 统一workmate的分隔符，逗号,删除空格
            parameter['workmate'] = request.POST['workmate'].replace("，", ",")
            parameter['workmate'] = re.sub("\s","",parameter['workmate'])

            User.objects.filter(id=request.session['uid']).update(**parameter)
            return HttpResponseRedirect("/notebook/user/info")
