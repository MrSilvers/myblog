from django.shortcuts import render,redirect
from django.template import loader,Context
from django.http import HttpResponse
from blog.models import BlogPost
import markdown
from blog.forms import BlogPostForm
from django.core.paginator import Paginator
from comments.forms import CommentForm
from comments.models import Comment

# Create your views here.


# 过滤markdown关键字符
def blogs_format(posts):
    for post in posts:
        post_temp = '' 
        for s in post.body[:70]: # 只过滤前70个字符
            if s not in ['#','*','~','>','-','']:
                post_temp += s # 把过滤好的字符加进来
        post.body = post_temp
    return posts

#该函数是实现了页面分页，它接收3个参数，依次是用户的request、
#从数据库取得的符合要求的blog以及人为设置的一页可显示的最大文章数目num
def page_button(request,post_list,num):
    paginator = Paginator(post_list,num)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return posts
 
 # 网站首页视图   
def archive(request):
    posts = blogs_format(BlogPost.objects.all()) # get all blog date from blog database
    
    '''posts_new = []
    for post in posts:
        post.body = markdown.markdown(post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                ])
        posts_new.append(post)
    context = {'posts':posts_new}
    '''
    context = {'posts':page_button(request,posts,10)}
    return render(request,'blog/index.html',context)


#原理：网页触发请求，指定app内的urls.py的path，再通
#过path，调用views.py内path指定的函数，最后return

# 博客详情视图
def archive_detail(request,id):
    #把posts全部读取后，list2页面实际上已经获得了每
    #一个blogpost的信息，当然也知道每一个blog的id，
    #点击title后，通过urls.py的path的调用指定函数的请求，并
    #传递指定函数的参数（blog的id），函数通过此id重
    #新从数据库获得id对应的blog，并将他显示
    post = BlogPost.objects.get(id = id)
    #post.body= markdown.markdown(post.body,
    #				extensions=[
  	#			  		#常用拓展
 	#			   		'markdown.extensions.extra',
    #					#语法高亮拓展
    #					'markdown.extensions.codehilite',
    #					'markdown.extensions.toc',
    #				])
    md = markdown.Markdown(extensions=[
         'markdown.extensions.extra',
         'markdown.extensions.codehilite',
         'markdown.extensions.toc',
    ])
    
    post.increase_views()
    post.body = md.convert(post.body)
    form = CommentForm()
    #获取这篇post下的全部评论
    comments = Comment.objects.filter(blog=id)
    #动态的给post对象绑定toc属性，不建议这样做
    #更加合理的是直接把toc传给context字典
    #post.toc = md.toc
    context = {'post':post,'toc':md.toc,'comments_list':comments,'form':form}
    return render(request,'blog/detail.html',context)

# 归档处理视图
def blog_list_by_date(request,year,month):
    posts = blogs_format(BlogPost.objects.filter(timestamp__year=year,
                                    timestamp__month=month
                                    ).order_by('-timestamp'))
    #context = {'posts':posts}
    context = {'posts':page_button(request,posts,10)}
    return render(request,'blog/index.html',context)
    
 # 分类处理视图
def blog_list_by_category(request,category):
    posts = blogs_format(BlogPost.objects.filter(category__name=category
                                    ).order_by('-timestamp'))
    #context = {'posts':posts}
    context = {'posts':page_button(request,posts,10)}
    return render(request,'blog/index.html',context)
# 关于我视图
def about_me(request):
    return render(request,'blog/about.html')

# 博客页面视图
def blog_index(request):
    posts = blogs_format(BlogPost.objects.all())#get all blog date from blog database
    context = {'posts':page_button(request,posts,10)}
    return render(request,'blog/blog.html',context)

'''def create_blog(request):
    if request.method == "POST":
        #将提交的数据赋值到表单实例中
        blog_post_form = BlogPostForm(data=request.POST)
        #如果提交的内容合法
        if blog_post_form.is_valid():
            #保存数据，不提交
            new_blog = blog_post_form.save(commit=False)
            #保存数据，默认提交
            new_blog.save()
            #跳转网页到blog-list
            return redirect("blog:blog_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    #如果用户请求数据（打开创建blog的网页这个动作即为请求）
    else:
        #创建默认的（空的）表单类实例
        blog_post_form = BlogPostForm()
        #赋值上下文
        context = {'blog_post_form':blog_post_form}
        return render(request,'blog/createblog2.html',context)

def delete_blog(request,id):
    #根据id获取需要删除的文章
    blog = BlogPost.objects.get(id=id)
    blog.delete()
    return redirect("blog:blog_list")

def update_blog(request,id):
    #从数据库取得要修改的文章对象
    blog = BlogPost.objects.get(id=id)
    #判断用户是否提交表单数据（已修改完后）
    if request.method == 'POST':
        #创建表单实例对象
        blog_post_form = BlogPostForm(data=request.POST)
        #如果数据合法，将http传递的request直接保存到blog对象中，而没有使用表单对象的数据（虽然是一样的），这样做显然不是很安全，待修改
        if blog_post_form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            blog.save()
            return redirect('blog:blog_detail',id=id)
        else:
            return HttpResponse("表单存在不合法内容，请修改。")
    else :
        blog_post_form = BlogPostForm()
        context = {'blog':blog,'blog_post_form':blog_post_form,}
        return render(request,'userprofile/update2.html',context)
'''
