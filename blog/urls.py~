#coding:utf8
from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('',views.archive,name='blog_list'),
    path('blog-detail/<int:id>/',views.archive_detail,name='blog_detail'),
    path('blog-list/<int:year>/<int:month>/',views.blog_list_by_date,name='blog_list_by_date'),
    path('blog-list/<str:category>/',views.blog_list_by_category,name='blog_list_by_category'),
    path('about/',views.about_me,name='about_me'),
    path('blog/',views.blog_index,name='blog'),
    #path('blog-create/',views.create_blog,name='blog_create'),
    #path('blog-delete/<int:id>/',views.delete_blog,name="blog_delete"),
    #path('blog-update/<int:id>/',views.update_blog,name="blog_update"),
]
