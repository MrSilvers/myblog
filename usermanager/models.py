from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
#为了能够使用django自带的login功能，这里同时使用uid作为用户的密码保存在本地
class UserInfo(models.Model):
    uid = models.CharField(max_length=64)#微博关联的uid
    password = models.CharField(max_length=128)
    #nickname = models.CharField(max_length=30,null=True)#用户昵称
    #head = models.CharField(max_length=100,null=True)#用户头像地址
    #sex = models.CharField(max_length=2,null=True)#性别
    #register_time= models.DateTimeField(default=timezone.now)#注册本站时间
    def save(self, *args, **kwargs):
        fields = kwargs.pop('update_fields', [])
        if fields != ['last_login']:
            return super(UserInfo, self).save(*args, **kwargs)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('uid',)

admin.site.register(UserInfo,UserInfoAdmin)
