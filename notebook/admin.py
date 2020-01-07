from django.contrib import admin
from notebook.models import User,Note,Log
  
#User模型的管理器
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'passwd')

#Log模型的管理器
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display=('id', 'user','createTime', 'url')

#Note模型的管理器
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'title','note_type','basedir_id','deleted')
    #list_display=('id', 'user', 'title','note_type','basedir_id','deleted','content')
