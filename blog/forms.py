from .models import BlogPost
from django import forms

class BlogPostForm(forms.ModelForm):
    class Meta:
        #指明数据模型来源
        model = BlogPost
        #定义表单包含的字段
        fields = ('title','body')
