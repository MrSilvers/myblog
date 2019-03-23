from django.shortcuts import render,redirect
from usermanager.models import UserInfo as WB_UserInfo
from usermanager.wb_oauth import OAuthWB
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
import time
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def weibo_login(request):
    url1 = ('https://api.weibo.com/oauth2/authorize?client_id=' + 
        settings.WEIBO_APP_ID + '&redirect_uri' + 
        settings.WEIBO_REDIRECT_URI)
    url2 = "https://api.weibo.com/oauth2/authorize?client_id="+settings.WEIBO_APP_ID+"&response_type=code&redirect_uri="+settings.WEIBO_REDIRECT_URI
    return HttpResponseRedirect(url2)
    
def weibo_get_code(request):
    #登录后会跳转到这里，获取授权吗code
    code = request.GET.get('code',None)
    sina = OAuthWB(settings.WEIBO_APP_ID,
                   settings.WEIBO_APP_KEY,
                   settings.WEIBO_REDIRECT_URI)
    try:
        user_access_token = sina.get_access_token(code)
        time.sleep(0.1)
    except:
        data = {}
        data['goto_url'] = 'blog/'
        data['goto_time'] = 10000
        data['goto_page'] = True
        data['message_title'] = '登录失败'
        data['message'] = "获取授权失败，请确认是否允许授权，并重试。"
        return render('usermanager/response.html',data)
    print(user_access_token)
    print(settings.WEIBO_APP_ID)
    #验证用户是否存在本地数据库信息
    user = authenticate(username=user_access_token['uid'],password=user_access_token["uid"])
    print(user)
    
    if user:
        login(request,user)
        return redirect("blog:blog_list")

    else :#用户第一次登录，保存用户信息到数据库
        new_user_info = sina.get_user_info(user_access_token)
        print(new_user_info)
        user_dict = {
            'uid':new_user_info['id'],
            'password':new_user_info['id'],#同时使用uid作为用户的本地密码
            #'nickname':new_user_info['name'],
        }
        try:
            new_user = WB_UserInfo.objects.create_user(username=user_dict['uid'],password=user_dict['password'])
            new_user.save()
        except Exception:
            return HttpResponse('保存失败')
        
        else:
            request.session['username'] = new_user_info['name']
            login(request,new_user)
            return redirect("blog:blog_list")
            

def user_logout(request):
    try:
        logout(request)
    except KeyError:
        pass
    return redirect("blog:blog_list")
    
