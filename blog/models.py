from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    #models.CASCADE的作用是当引用的外键的对象被删除时，本对象也级联删除，django2.0必须传入此参数
    category = models.ForeignKey(Category,default='',on_delete=models.CASCADE)
    #一个标签可以有多篇文章，一篇文章也可能有多个标签，是多对多的关系
    tags = models.ManyToManyField(Tag,default='',blank=True)
    views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-timestamp',)
    
    #粗略的对文章访问计数，可能存在多个人同时访问不能准确计数的问题
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    def get_absolute_url(self):
        return reverse('blog:blog_detail',args=[self.id])

