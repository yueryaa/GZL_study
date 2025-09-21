# -*- coding: utf-8 -*-
# @Time    : 2024-01-07 15:34
# @Author  : yuer
# @FileName: User_detail.py
# @Software: PyCharm

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from gzl.models import User, Likes, Artical,Favorites
from gzl.serializers import Userserializer

@api_view(["POST"])
def login(request):
    """
    登录
    :param request: account password
    :return: msg state
    """
    account = request.data.get('account')
    print(account)
    pwd = request.data.get('password')
    t = User.objects.filter(account=account)
    if t.exists():
        state = t.first().uid,
        data = t.first().password
        msg = '登录成功'
    else:
        state = 0,
        msg = '请进行注册'
        data=0
    return JsonResponse(data={
        'state': state,
        'msg': msg,
        'pwd':data
        })

@api_view(["POST"])
def signup(request):
    """
    注册
    :param request: account password name
    :return: state msg
    """
    account = request.data.get('account')
    pwd = request.data.get('password')
    name = request.data.get('name')
    email = request.data.get('email')
    picture = request.data.get('picture')
    t = User.objects.filter(account=account)
    if t.exists():
        state = 0,
        msg = '已有账号，请进行登录'
    else:
        user = User(account=account, password=pwd, name=name,email=email,picture=picture)
        user.save()
        state = t.first().uid
        msg = '注册成功'
    return JsonResponse(data={
        'state': state,
        'msg': msg})

class UserDetail(APIView):
    """
    修改个人信息
    """
    @staticmethod
    def get_object(id):
        """
        获取user对象
        :param id:
        :return: user对象
        """
        try:
            return User.objects.get(uid=id)
        except User.DoesNotExist:
            return

    def get(self, request):
        """
        获取个人信息
        :param request: id
        :return:uid password name account picture remark brithday likeCount postCount collectCount
        """
        obj = self.get_object(request.GET.get("id"))
        if not obj:
            return Response(data={"msg": "没有个人信息"}, status=status.HTTP_404_NOT_FOUND)
        s = Userserializer(instance=obj)
        post = Artical.objects.filter(uid=request.GET.get("id"))
        postCount = post.count()
        d = list(post.values('aid'))
        a = []
        for it in d:
            a.append(it['aid'])
        likeCount = Likes.objects.filter(aid__in=a).count()
        collectCount = Favorites.objects.filter(aid__in=a).count()
        b = s.data
        b['postCount'] = postCount
        b['likeCount'] = likeCount
        b['collectCount'] = collectCount
        return Response(data=b, status=status.HTTP_200_OK)

    def put(self, request):
        """
        更新个人信息
        :param request: id password name account picture remark brithday
        :return: msg/data
        """
        obj = self.get_object(request.data.get("uid"))
        # 没有查询到 obj是空值
        if not obj:
            return Response(data={"msg": "没有个人信息"}, status=status.HTTP_404_NOT_FOUND)
        s = Userserializer(instance=obj, data=request.data)  # 反序列化
        if s.is_valid():
            s.save()
            return Response(data={"msg": "更新成功"}, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_pic(request):
    """
    用户头像获取
    :param request: id
    :return:
    """
    try:
        obj = User.objects.get(uid=request.GET.get('id'))
        s = Userserializer(instance=obj).data.get("picture")
        return Response(data={'picture': s}, status=status.HTTP_200_OK)
    except:
        return Response(data={'picture': "没有个人信息"}, status=status.HTTP_404_NOT_FOUND)
