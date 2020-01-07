from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import parse_message, create_reply
from wechatpy.replies import BaseReply
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth
from django.shortcuts import redirect
from wechatpy.replies import TextReply, ArticlesReply

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64


def decrypt(ciphertext):
    return str(base64.b64decode(bytes.fromhex(ciphertext)), encoding='utf8')


def send_email(subject="", content="", to="65117032@qq.com"):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "dhs789520@qq.com"
    mail_pass = decrypt('password')

    sender = 'dhs789520@qq.com'
    receivers = [to, ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 定义消息内容，来源，去处，主题
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("戴辉水", 'utf-8')
    message['To'] = Header(to, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


WECHAT_TOKEN = 'dhs789520'
AppID = 'wxd638d1da36c53aac'
AppSecret = '90969c6c2ec38a521b9a3b9637fe3d91'


# 连接小程序的方法
def miniPrograme(request):
    # GET 方式用于微信公众平台绑定验证
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        print(WECHAT_TOKEN, signature, timestamp, nonce)
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求!!!!'
        return HttpResponse(echo_str)
    else:
        msg = parse_message(request.body)
        # print("消息类型:",msg.type)
        # print("事件:",msg.event)
        print("消息:", msg)

        reply = TextReply(message=msg)

        if msg.type == 'event':
            if msg.event == 'subscribe':
                print("新用户订阅:%s" % msg.source, dir(msg))
                reply.content = "无论如何，都欢迎您！"
            elif msg.event == 'unsubscribe':
                print("用户取消订阅:%s" % msg.source, dir(msg))
                reply.content = "下次再来1！"
        elif msg.type == 'text':
            reply.content = msg.content
            # reply = ArticlesReply(message=msg)
            # reply.add_article({
            # 'title':'test',
            # 'description':'des of test',
            # 'image':'http://linux.zicp.vip/static/images/logo.png',
            # 'url':'http://linux.zicp.vip'
            # })
        elif msg.type == 'image':
            reply.content = "您发了一张图片吗？图片的地址为:%s" % msg.image
        elif msg.type == 'voice':
            reply.content = "您发了一条语音吗？"
        elif msg.type == 'video':
            reply.content = "您发了一个视频吗？"
        elif msg.type == 'location':
            reply.content = "您发了一个地理位置吗？纬度：%s-经度:%s,位置:%s" % (
                msg.location_x, msg.location_y, msg.label)
        elif msg.type == 'shortvideo':
            reply.content = "您发了一个短视频吗？"
        elif msg.type == 'link':
            reply.content = "您发了一个链接吗？链接:%s ,地址:%s" % (
                msg.description, msg.url)

        xml = reply.render()
        return HttpResponse(xml)


# 连接微信公众号的方法
def server(request):
    # GET 方式用于微信公众平台绑定验证
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        # print(WECHAT_TOKEN, signature, timestamp, nonce)
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '微信订阅号：错误的请求!!!'
        return HttpResponse(echo_str)
    else:
        msg = parse_message(request.body)
        # print("消息类型:",msg.type)
        # print("事件:",msg.event)
        # print("消息:", msg)

        reply = TextReply(message=msg)

        if msg.type == 'event':
            # print(msg.event)
            if 'subscribe' in msg.event and (msg.event != "unsubscribe"):
                # print("新用户订阅:%s" % msg.source, dir(msg))
                send_email(subject="新用户订阅!", content="新用户订阅")
                reply.content = "欢迎您来到重症医学质量控制，在后台回复消息，可获得重症医学相关知识！"
            elif msg.event == 'unsubscribe':
                # print("用户取消订阅:%s" % msg.source, dir(msg))s
                reply.content = "下次再来1！"
        elif msg.type == 'text':
            reply.content = msg.content
            # reply = ArticlesReply(message=msg)
            # reply.add_article({
            # 'title':'test',
            # 'description':'des of test',
            # 'image':'http://linux.zicp.vip/static/images/logo.png',
            # 'url':'http://linux.zicp.vip'
            # })
        elif msg.type == 'image':
            reply.content = "您发了一张图片吗？图片的地址为:%s" % msg.image
        elif msg.type == 'voice':
            reply.content = "您发了一条语音吗？"
        elif msg.type == 'video':
            reply.content = "您发了一个视频吗？"
        elif msg.type == 'location':
            reply.content = "您发了一个地理位置吗？纬度：%s-经度:%s,位置:%s" % (
                msg.location_x, msg.location_y, msg.label)
        elif msg.type == 'shortvideo':
            reply.content = "您发了一个短视频吗？"
        elif msg.type == 'link':
            reply.content = "您发了一个链接吗？链接:%s ,地址:%s" % (
                msg.description, msg.url)

        xml = reply.render()
        return HttpResponse(xml)


if __name__ == "__main__":
    pass
