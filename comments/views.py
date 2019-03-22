from django.shortcuts import render,get_object_or_404,redirect
from blog.models import BlogPost
from .models import Comment
from .forms import CommentForm
from django.http import HttpResponse
from usermanager.models import UserInfo
# Create your views here.

def post_comment(request,blog_id):
    #要获取的文章存在时则获取，否则返回404页面
    post = get_object_or_404(BlogPost,pk=blog_id)

    if request.method == 'POST':
        #通过request.post的数据生成表单对象
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            #将评论和被评论的文章关联起来
            new_comment.blog = post
            new_comment.user = request.user
            new_comment.save()
            return redirect(post)
        else :
            '''comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list,
                        }
            return render(request,'blog/detail.html',context=context)
            '''
            return HttpResponse('表单内容不合法')

    #redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实
    #例作为参数（例如这里的 post）。如果接收一个模型的实例，那么这
    #个实例必须实现了 get_absolute_url 方法，这样 redirect 会根据
    #get_absolute_url 方法返回的 URL 值进行重定向
    return redirect(post)
