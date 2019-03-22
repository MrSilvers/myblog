from django.db import models
from blog.models import BlogPost
from usermanager.models import UserInfo

# Create your models here.

class Comment(models.Model):
    #指定外键的表名就默认引用外键表的id属性
    blog = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        
    )
    user = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[:20]
