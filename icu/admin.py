from django.contrib import admin

from icu.models import guestbook,ApacheII,QualityControl,Bilingual

#guestbook模型的管理器
@admin.register(guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display=('id', 'contact', 'content','public','create_time')


#ApacheII模型的管理器
@admin.register(ApacheII)
class ApacheIIAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'inNumber','createTime','score','deathRate','doctor')

#QualityControl模型的管理器
@admin.register(QualityControl)
class QcAdmin(admin.ModelAdmin):
    list_display=('id', 'total', 'qcDate')


#Bilingual模型的管理器
@admin.register(Bilingual)
class BilingualAdmin(admin.ModelAdmin):
    list_display=('id', 'src','length','doctor','ip')
