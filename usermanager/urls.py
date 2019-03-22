from django.urls import path
from usermanager import views

app_name = 'usermanager'

urlpatterns = [
    path('login/',views.weibo_login,name="login"),
    path('login/process',views.weibo_get_code,name='process'),
    path('logout/',views.user_logout,name='logout')
]
