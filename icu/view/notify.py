#!/usr/bin/python3
from django.shortcuts import render, render_to_response
# from django.http import HttpResponse as HR
# from django.http import HttpResponseRedirect
# from django.http import StreamingHttpResponse
# from django.db.models import Q
from icu.models import guestbook as gs
from settings import BASE_DIR
import os
import base64
import random
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 设置主页及一些静态内容模板的返回


def index(request, keyword):

    # 默认主页为index
    if not keyword:
        keyword = "index"
    template = "icu/notify/" + keyword + ".html"
    return render(request, template)

# 设定留置板功能


def guestbook(request):
    if request.method == 'POST':

        # 获取用户信息
        agent = request.META.get('HTTP_USER_AGENT', '')  # 浏览器信息
        ip = request.META.get('REMOTE_ADDR', '')  # IP地址
        message = {}
        message['contact'] = request.POST['contact']
        message['content'] = request.POST['content']
        gs.objects.create(contact=request.POST['contact'],
                          content=request.POST['content'],
                          ip=ip,
                          agent=agent)

        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        mail_message = MIMEText(request.POST['content'], 'html', 'utf-8')
        mail_message['From'] = Header("患者家属留言", 'utf-8')   # 发送者
        mail_message['To'] = Header("管理员", 'utf-8')        # 接收者
        water = [
            "65117032@qq.com", str(
                base64.b64decode(
                    bytes.fromhex('password')), encoding='utf8')]

        subject = '患者家属留言'
        mail_message['Subject'] = Header(subject, 'utf-8')
        email = smtplib.SMTP("smtp.qq.com", 25)
        email.login(water[0], water[1])
        email.sendmail(
            "65117032@qq.com", [
                "65117032@qq.com", ], mail_message.as_string())
        email.quit()

        template = "icu/notify/message_success.html"
        return render(request, template, {'message': message})
    else:
        # 管理留言板界面
        if request.GET.get('show') == 'all':
            # 先处理对留言的处理动作
            if request.GET.get('action') == 'public':
                gs.objects.filter(id=request.GET['id']).update(public=True)
            elif request.GET.get('action') == 'hide':
                gs.objects.filter(id=request.GET['id']).update(public=False)
            elif request.GET.get('action') == 'answer':
                gs.objects.filter(
                    id=request.GET['id']).update(
                    answer=request.GET['answer'])

            messages = gs.objects.all().order_by("-id")
            template = "icu/notify/guestbook_admin.html"
        # 普通界面
        else:
            messages = gs.objects.filter(public=True).order_by("-id")[0:50]
            template = "icu/notify/guestbook.html"
        return render(request, template, {'messages': messages})

# 计算今日值班状态


def on_duty(request):
    # 医生列表
    doctors = [
        {'name': '戴辉水', 'job': '主治医师（科副主任）', 'img': 'dhs.jpg'},
        {'name': '吕  嵩', 'job': '主治医师', 'img': 'ls.jpg'},
        {'name': '吕明生', 'job': '主治医师', 'img': 'lms.jpg'},
        {'name': '沈正奎', 'job': '主治医师', 'img': 'szk.jpg'},
        {'name': '姬楚睿', 'job': '住院医师', 'img': 'jcr.jpg'},
        {'name': '吴德清', 'job': '住院医师', 'img': 'wdq.jpg'},
        # {'name':'陈玉文','job':'住院医师','img':'cyw.jpg'},
    ]

    doctors[0]['introduce'] = '重症医学科（ICU）副主任、主持工作，主治医师。2008年毕业于皖南医学院，医学学士。2012年于广东南海区中医院进修深造。2018年于蚌埠医学院第一附属医院进修学习。专科特长：擅于重症相关操作、急危重症病人急救和呼吸、循环系统监护和治疗。对心肺脑复苏、重症肺炎、急性呼吸窘迫综合征（ARDS）、重症外伤、重症脑卒中等多种危重病的治疗有丰富的临床经验和较强的理论功底。'
    doctors[1]['introduce'] = '主治医师  2006年毕业于蚌埠医学院临床医学系 ，医学学士学位 ，自参加工作一直从事普内科临床工作，并于2014-2015年度在安徽省省立医院呼吸内科进修学习。专业特长：对慢性阻塞性肺疾病 支气管哮喘 支气管扩张 肺栓塞 肺部感染性疾病的诊治、对呼吸衰竭的有创和无创机械通气治疗有丰富的临床经验。'
    doctors[2]['introduce'] = '主治医师，2006年毕业于皖南医学院临床医学系，学士学位，曾在中国人民解放军总医院（301医院）进修学习，2009年获得安徽省院前急救技能大赛“优秀选手”称号，在医学期刊上发表论文一篇。专业特长：内外科常见病多发病的诊治，急危重症的救治及脏器功能支持，人工气道的建立及管理。'
    doctors[3]['introduce'] = '主治医师，2006年毕业于安徽理工大学医学院，2017年毕业于贵州医科大学，临床型硕士，急诊医学专业。专业特长：内外科急诊、急诊危重症处理、中毒及呼吸心跳骤停救治。'

    date = datetime.date.today()
    basedate = datetime.datetime.strptime("20181027", "%Y%m%d").date()
    weekday = date.weekday() + 1
    weekday_cn = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
    work_cycle = (date - basedate).days % 4

    # 设定进修人员工作时间
    # 吕嵩1，吴德清5
    doctors[5]['on_time'] = '本月外出进修'

    # 设定常白班人员工作时间
    # 戴辉水0
    if weekday < 6:
        doctors[0]['on_time'] = '白班 在岗时间 8:00-12:00 14:30-17:30'
        #doctors[6]['on_time']='白班 在岗时间 8:00-12:00 14:30-17:30'
    elif weekday == 6:
        doctors[0]['on_time'] = '白班 在岗时间 8:00-12:00'
        #doctors[6]['on_time']='白班 在岗时间 8:00-12:00'
    else:
        doctors[0]['on_time'] = '今日休息'
        # doctors[6]['on_time']='今日休息'

    # 设定常值班人员工作时间
    # 吕明生2，吕嵩1，沈正奎3，姬楚睿4

    if work_cycle == 0:
        doctors[2]['on_time'] = '今日夜班 在岗时间 中午12:00后全天在岗'
        doctors[4]['on_time'] = '今日值班 在岗时间 昨夜至中午12:00'
        doctors[1]['on_time'] = '今日休息'
        doctors[3]['on_time'] = '今日白班 在岗时间 8:00-12:00 14:30-17:30'
    elif work_cycle == 1:
        doctors[3]['on_time'] = '今日夜班 在岗时间 中午12:00后全天在岗'
        doctors[2]['on_time'] = '今日值班 在岗时间 昨夜至中午12:00'
        doctors[4]['on_time'] = '今日休息'
        doctors[1]['on_time'] = '今日白班 在岗时间 8:00-12:00 14:30-17:30'
    elif work_cycle == 2:
        doctors[1]['on_time'] = '今日夜班 在岗时间 中午12:00后全天在岗'
        doctors[3]['on_time'] = '今日值班 在岗时间 昨夜至中午12:00'
        doctors[2]['on_time'] = '今日休息'
        doctors[4]['on_time'] = '今日白班 在岗时间 8:00-12:00 14:30-17:30'
    elif work_cycle == 3:
        doctors[4]['on_time'] = '今日夜班 在岗时间 中午12:00后全天在岗'
        doctors[1]['on_time'] = '今日值班 在岗时间 昨夜至中午12:00'
        doctors[3]['on_time'] = '今日休息'
        doctors[2]['on_time'] = '今日白班 在岗时间 8:00-12:00 14:30-17:30'

    template = "icu/notify/on_duty.html"
    return render(
        request, template, {
            'doctors': doctors, 'date': date, 'weekday': weekday_cn[weekday], })
