# -*- coding: utf-8 -*-
# @Time    : 2023-12-08 22:58
# @Author  : yuer
# @FileName: fun.py
# @Software: PyCharm

from django.db import connection


# cursor是执行sql_str后的记录，作入参
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description] # 得到域的名字col[0]，组成List
    return [
        dict(zip(columns, row)) for row in cursor.fetchall() #
    ]

def artical_detail(sql_str):
    with connection.cursor() as cursor:  # with语句用于数据库操作
        cursor.execute(sql_str)
        dataInfo = dict_fetchall(cursor)
    for item in dataInfo:
        aid = item['aid']
        sql_like = "select User.name,User.uid from Likes,User where User.uid=Likes.uid and Likes.aid=" + str(aid)
        sql_comment = "select User.name,comment.content  from User,comment where User.uid=comment.uid and comment.aid=" + str(aid)
        sql_favorites="select User.name,User.uid  from User,favorites where User.uid=favorites.uid and favorites.aid=" + str(aid)
        with connection.cursor() as cursor:  # with语句用于数据库操作
            cursor.execute(sql_like)
            like = dict_fetchall(cursor)
        with connection.cursor() as cursor:  # with语句用于数据库操作
            cursor.execute(sql_comment)
            comment = dict_fetchall(cursor)
        with connection.cursor() as cursor:  # with语句用于数据库操作
            cursor.execute(sql_favorites)
            favorites = dict_fetchall(cursor)
        item['likeList']=like
        item['commentList'] = comment
        item['favoritesList']=favorites
    return dataInfo