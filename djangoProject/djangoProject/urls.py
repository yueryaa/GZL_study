"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# url和函数的对应关系

# python manage.py inspectdb > gzl/models.py
# python manage.py inspectdb

from django.urls import path
from rest_framework.documentation import include_docs_urls
from gzl.views import Group_detail, Rank, Article_detail,User_detail


urlpatterns = [
    # 路由
    path('docs/', include_docs_urls(title="DRF API文档")),
    # path("first/",include(router.urls))
    # 用户登录
    path('login/', User_detail.login),
    # 用户注册
    path('signup/', User_detail.signup),
    # 用户管理
    path('UserDetail/', User_detail.UserDetail.as_view()),
    # 返回用户头像
    path('file/getAvatar/', User_detail.get_pic),

    # 查看小组成员
    path('user_group/', Group_detail.user_group),
    # 对小组中成员进行管理
    path('User_GroupDetail/', Group_detail.User_GroupDetail.as_view()),
    # 创建小组
    path('creat_group/', Group_detail.creat_group),
    # 申请加入小组
    path('ApplicationDetail/', Group_detail.ApplicationDetail.as_view()),

    # 排行榜
    path('rankArtical/', Rank.rankArtical),
    path('rankLike/', Rank.rankLike),

    # 文章
    path('ArticalDetail/', Article_detail.ArticalDetail.as_view()),
    path('loadArctial/' , Article_detail.loadArctial),
    path('getownArtical/', Article_detail.getownArtical),
    path('getownlikeArtical/', Article_detail.getownlikeArtical),
    path('getowncollectArtical/', Article_detail.getowncollectArtical),
    # 点赞 收藏 评论
    path('likeArtical/', Article_detail.likeArtical.as_view()),
    path('collectArtical/', Article_detail.collectArtical.as_view()),
    path('commentArtical/', Article_detail.commentArtical),
    # 通知
    path('interaction_info/', Article_detail.interaction_info.as_view()),

]
