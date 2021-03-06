from ..models import BlogPost,Category,Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return BlogPost.objects.all().order_by('-timestamp')[:num]

@register.simple_tag
def archives():
    return BlogPost.objects.dates('timestamp','month',order='DESC')

@register.simple_tag
def get_categories():
    #blogpost是什么对象？？？
    return Category.objects.annotate(num_posts=Count('blogpost')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('blogpost')).filter(num_posts__gt=0)



