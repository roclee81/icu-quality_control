from django.db import models
import django.utils.timezone as timezone
# Create your models here.
'''
知识库管理模型
为了更好地终身管理知识，特创建知识库管理
知识库管理是这样一个工具
1.它记录您曾经学过的知识
2.它记录您想要学习的知识
3.它对您学习过的知识分类
4.它支持对您的知识使用关键字/时间/内容 搜索
5.支持多用户同时使用此数据库
6.无级分类，支持树状目录


'''


class User(models.Model):
    '''
    为了支持多用户
    '''
    name = models.CharField(max_length=30,unique=True)
    #呢称
    nickName = models.CharField(max_length=30,null=True)
    #密码
    passwd = models.CharField(max_length=25,null=True)# password for login
    #紧急密码
    intensive_passwd = models.CharField(max_length=30,null=True) #passwd for some important notes


    #Email、QQ、Wechat、Phone
    email = models.EmailField(null=True)
    qq = models.IntegerField(null=True)
    wechat = models.IntegerField(null=True)
    phone = models.IntegerField(null=True)

    #用户等级,用来提示用户的操作级别，权限
    degree = models.IntegerField(null=True,default=0)


    #工作单位,hospital
    company = models.CharField(max_length=45,null=True,default="")
    #部门
    department = models.CharField(max_length=45,null=True,default="")
    #部门照片名称
    departmentImg = models.CharField(max_length=45,null=True,default="")
    #同事列表，用“，”做分隔
    workmate = models.CharField(max_length=300,null=True,default="")
    #真实姓名
    real_name = models.CharField(max_length=30,null=True)

    #注册时间
    create_time = models.DateTimeField(default=timezone.now)
    #排列方式
    sort_rank = models.IntegerField(default = 0)
    #login_time = 
    #login_ip= 
    #display=
    #edit_habit=

    def __str__(self):
        return self.name
    
class Log(models.Model):
    '''
    用户行为日志
    主要记录 用户名，登录IP，浏览URL
    '''
    user = models.CharField(max_length=100,db_index=True)
    #URL路径
    url = models.CharField(max_length=100,null=True,db_index=True)
    #IP
    ip = models.CharField(max_length=40,null=True)
    #agent
    agent = models.CharField(max_length=100,null=True)
    #浏览时间 ，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user

class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #条目类型标记 0文件夹 1 普通笔记
    note_type = models.IntegerField(default = 0)
    #basedir = models.ForeignKey('self',related_name='son_notes',default = 0,verbose_name='父目录')
    #父目录的id，因为默认可以不存在的父目录 0，所以不能设置外键为本身
    basedir_id = models.IntegerField(default = 0)
    title = models.CharField(max_length=500)
    keywords = models.CharField(max_length=100,null=True)
    content = models.TextField(null=True,blank=True)
    public = models.BooleanField(default=True)
    #创建时间
    create_time = models.DateTimeField(default=timezone.now)
    #修改时间
    update_time = models.DateTimeField(default=timezone.now)
    #浏览时间
    retrieve_time = models.DateTimeField(default=timezone.now)
    #删除时间
    delete_time = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    #分享标记 0不分享 1分享
    share = models.IntegerField(default = 0)
    share_passwd = models.CharField(max_length=25,null=True)# password for login
    click_times = models.IntegerField(default = 0)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id',]


'''
我的实验室
用于帮助论文写作者存储数据，数据都为论文常用数据
结构化存储在线数据，可以使论文数据复用
修改容易，
并且目标是可以通过结果逆向生成数据功能
'''

'''
实验室，与用户关联，存储每一个实验室数据
'''
class Stats_lab(models.Model):
    #用户，每一个实验室关联一个用户
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #实验室标题，表明是什么样的实验室
    title = models.CharField(max_length=100)

    #实验设计描述
    #描述实验设计思路等一系列情况
    describe = models.TextField(null=True,blank=True)

    #实验结果
    result = models.TextField(null=True,blank=True)

    #实验室是否公开，默认为False
    public = models.BooleanField(default=False)

    #实验设计被点赞数
    thumbs_up = models.IntegerField(default = 0)

    #删除标记
    #用户数据删除只做标记，不做删除
    deleted = models.BooleanField(default=False)

    #创建时间，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id',]

'''
实验数据组，与实验室关联，存储实验室的每一个实验组数据
'''
class Stats_group(models.Model):
    #实验室，每一个实验组关联一个实验室
    lab = models.ForeignKey(Stats_lab,on_delete=models.CASCADE)

    #数据组标题，表明是什么样的实验组，如对照组，实验组等等
    title = models.CharField(max_length=100)

    #实验小组描述
    #描述实验小组情况
    describe = models.TextField(null=True,blank=True)

    #平均值 浮点数类型
    avg = models.FloatField(null=True)

    #4:标准差 浮点数类型
    std = models.FloatField(null=True)


    #创建时间，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id',]


'''
实验数据，与实验组关联，存储实验室的每一个实验组数据
'''
class Stats_data(models.Model):
    #实验组，每一个实验组关联一个实验室
    group = models.ForeignKey(Stats_group,on_delete=models.CASCADE)

    #数据标题，表明是什么样的单个数据，如计数资料的 阳性、阴性；等级资料的+、++、+++
    title = models.CharField(null=True,max_length=50)

    '''
    数据类型
    数据类型枚举：
    0:整数类型计量数据
    1:浮点数类型计量数据
    2:整数类型计数资料数据

    '''
    data_type = models.IntegerField(default = 1) # 默认为浮点数计量数据

    #0:整数类型计量资料 
    data_int = models.IntegerField(null=True)
    #1:浮点数类型计量资料
    data_float = models.FloatField(null=True)

    #2:整数类型计数资料 
    data_enum = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id',]


'''
经典名句，用来呈现每日一句的
内容和灵感从Linux的fortun中得来，因此同名
'''
class Fortune(models.Model):
    #类型，一般有 中文，英文，古诗等
    title = models.CharField(max_length=50)
    content = models.TextField(unique=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['id',]
