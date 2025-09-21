# -*- coding: utf-8 -*-
# @Time    : 2024-01-07 15:48
# @Author  : yuer
# @FileName: Rank.py
# @Software: PyCharm

from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from utils.fun import dict_fetchall

@api_view(["GET"])
def rankArtical(request):
    """
    小组发文数排序
    :param request:gid
    :return:uid name picture account count rank
    """
    gid = request.GET.get('gid')
    sql="select * from rank_artical where gid="+str(gid)
    with connection.cursor() as cursor:  # with语句用于数据库操作
        cursor.execute(sql)
        dataInfo = dict_fetchall(cursor)
    i = 0
    for item in dataInfo:
        item['rank'] = i + 1
        i += 1
    return Response(data=dataInfo, status=status.HTTP_200_OK)



@api_view(["GET"])
def rankLike(request):
    """
    小组点赞排序
    :param request:gid
    :return:uid name picture account count rank
    """
    gid = request.GET.get('gid')
    sql="select * from like_artical where gid="+str(gid)
    with connection.cursor() as cursor:  # with语句用于数据库操作
        cursor.execute(sql)
        dataInfo = dict_fetchall(cursor)
    i = 0
    for item in dataInfo:
        item['count']=int(item['count'])
        item['rank'] = i + 1
        i += 1
    return Response(data=dataInfo, status=status.HTTP_200_OK)

