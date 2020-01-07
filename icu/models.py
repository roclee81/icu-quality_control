from django.db import models
import django.utils.timezone as timezone
from notebook.models import User

# Create your models here.
'''
质控管理模型



'''

class guestbook(models.Model):
    '''
    ICU家属心声留言本
    '''
    #联系方式,可以不填
    contact = models.CharField(max_length=500,null=True)
    #留言内容，必须要填
    content = models.TextField()
    #回复内容，必须要填
    answer = models.TextField(null=True)
    #是否公开
    public = models.BooleanField(default=False)
    #创建时间
    create_time = models.DateTimeField(default=timezone.now)
    #客户IP
    ip = models.CharField(max_length=500,null=True)
    #客户浏览器
    agent = models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.content
    
#ApacheII用户信息存储数据库
class ApacheII(models.Model):
    #用户信息
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #患者姓名
    name = models.CharField(max_length=20)
    #患者年龄
    age = models.IntegerField()
    #床号作为字符，有加床的好处
    bedNumber = models.CharField(max_length=20)
    inNumber = models.IntegerField()
    temperature = models.FloatField()
    SBP = models.IntegerField()
    DBP = models.IntegerField()
    #平均动脉压，为计算值，一并存储
    MAP = models.FloatField()
    HR = models.IntegerField()
    R = models.IntegerField()
    WBC = models.FloatField()
    HCT = models.FloatField()
    pH = models.FloatField()
    FiO2 = models.FloatField()
    PaO2 = models.FloatField()
    PaCO2 = models.FloatField()
    #肺泡动脉氧分压差，为计算值，一并存储
    AaDO2 = models.FloatField()
    Na = models.FloatField()
    K = models.FloatField()
    Cr = models.FloatField()
    AKI = models.CharField(max_length=4)
    health = models.CharField(max_length=40)
    E = models.IntegerField()
    V = models.IntegerField()
    M = models.IntegerField()
    noSurgery = models.CharField(max_length=40)
    surgery = models.CharField(max_length=40)
    afterSurgery = models.CharField(max_length=20)
    #最终ApacheII评分
    score = models.FloatField()
    #死亡率
    deathRate = models.FloatField()
    #评分医生
    doctor = models.CharField(db_index=True,max_length=40)
    ip = models.CharField(max_length=40)
    #用户输入的打分时间
    scoreTime = models.DateTimeField(db_index=True,verbose_name='打分时间')
    #创建时间，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id',]


# 重症医学科 质量控制
class QualityControl(models.Model):
    #用户信息
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #质控日期
    qcDate = models.DateField(db_index=True,verbose_name='质控日期')

    #当前在科总人数
    total = models.IntegerField()
    #昨总入科人数
    entry = models.IntegerField()
    #门急诊转入
    outpatient = models.IntegerField()
    #病房转入
    shiftIn = models.IntegerField()
    #非计划转入
    unplannedShift = models.IntegerField()
    #48h重返
    revert = models.IntegerField()

    #所有总出科
    out = models.IntegerField()
    #转出他科
    transfer = models.IntegerField()
    #好转出院
    improve = models.IntegerField()
    #治愈出院
    cure = models.IntegerField()
    #自动出院
    automaticDischarge = models.IntegerField()
    #死亡
    death = models.IntegerField()

    #机械通气数
    ventilation = models.IntegerField()
    #新增VAP
    newVAP = models.IntegerField()
    #昨日新增插管
    newTracheaCannula = models.IntegerField()
    #非计划拨管 unplanned extubation
    unplannedExtubation = models.IntegerField()
    #48小时再插管
    reintubation = models.IntegerField()


    #动静脉导管总数
    AVCatheter = models.IntegerField()
    #新增动静脉导管相关血流感染
    CRBSI = models.IntegerField()

    #导尿管总数
    urethralCatheter = models.IntegerField()
    #新增导管相关尿路感染
    CAUTI = models.IntegerField()

    #感染性休克
    septicShock = models.IntegerField()
    #3小时Bundel
    bundle3 = models.IntegerField()
    #6小时Bundel
    bundle6 = models.IntegerField()

    #新增抗生素
    antibiotic = models.IntegerField()
    #标本送检
    sample = models.IntegerField()

    #新增DVT预防
    preventDVT = models.IntegerField()
    #新发DVT数
    newDVT= models.IntegerField()


    #备注日志
    comments = models.CharField(max_length=400)

    #评分医生
    doctor = models.CharField(max_length=40)
    ip = models.CharField(max_length=40)
    #创建时间，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.qcDate.strftime("%Y-%m-%d")

    class Meta:
        ordering = ['-id',]




# 英语学习语料数据库
class Bilingual(models.Model):
    #用户信息
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #源文本
    src = models.TextField()

    #源文本长度
    length= models.IntegerField()

    #翻译后文本
    dst = models.TextField()

    #双语文本
    bil = models.TextField()

    #评分医生
    doctor = models.CharField(max_length=40,null=True)
    #ip地址
    ip = models.CharField(max_length=40)

    #创建时间，自动生成
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.src[:50:]

    class Meta:
        ordering = ['-id',]















