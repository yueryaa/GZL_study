# -*- coding: utf-8 -*-
# @Time    : 2024-01-07 15:49
# @Author  : yuer
# @FileName: Article_detail.py
# @Software: PyCharm

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from gzl.models import User, Group,  Likes, Artical, Notice, Favorites, Comment
from gzl.serializers import Articalserializer
from django.db import connection
from utils.fun import dict_fetchall, artical_detail

class interaction_info(APIView):
    """
    进行通知
    """
    def get(self, request):
        """
        获取通知
        :param request: id
        :return: nid uid name ncontent ntime
        """
        uid = request.GET.get('id')
        sql_str = "select notice.nid,notice.uid,user.name,notice.ncontent,notice.ntime from notice,artical,user where notice.aid=artical.aid and user.uid=notice.uid and artical.uid=" + str(
            uid)
        with connection.cursor() as cursor:  # with语句用于数据库操作
            cursor.execute(sql_str)
            dataInfo = dict_fetchall(cursor)
        return Response(data=dataInfo, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        删除通知
        :param request: nid
        :return:msg status
        """
        obj = Notice.objects.filter(nid=request.GET.get("nid"))
        if not obj:
            return Response(data={"msg": "没有此通知信息"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(data={"msg": "删除成功"}, status=status.HTTP_200_OK)

class ArticalDetail(APIView):
    def post(self, request):
        """
        发文章
        :param request:atime id gid content imageurl
        :return:msg
        """
        atime = request.data.get('atime')
        id = User.objects.get(uid=request.data.get('id'))
        gid = Group.objects.get(gid=request.data.get('gid'))
        content = request.data.get('content')
        imageurl = request.data.get('imageurl')
        favorites_num=0
        like_num = 0
        comment_num = 0
        artical = Artical(atime=atime, uid=id, gid=gid, content=content, imageurl=imageurl,favorites_num=favorites_num,like_num=like_num,comment_num=comment_num)  #
        artical.save()
        msg = '发布成功'
        return JsonResponse(data={'msg': msg})

    def get(self, request):
        """
        获取文章
        :param request:aid
        :return:aid group_name User_name content favorites_num like_num comment_num atime imageurl uid gid
        """
        aid = request.GET.get('aid')
        artical = Artical.objects.get(aid=aid)
        data = Articalserializer(instance=artical).data
        return JsonResponse(data=data)

    def put(self, request):
        """
        更新文章
        :param request:aid uid gid content imageurl
        :return:mag status
        """
        obj = Artical.objects.get(aid=request.data.get("aid"))
        if not obj:
            return Response(data={"msg": "没有该信息"}, status=status.HTTP_404_NOT_FOUND)
        obj.uid = User.objects.get(uid=request.data.get("uid"))
        obj.gid = Group.objects.get(gid=request.data.get("gid"))
        obj.content = request.data.get("content")
        obj.imageurl = request.data.get("imageurl")
        obj.save()
        # 没有查询到 obj是空值
        # obj.update(uid=uid,gid=gid,content=content,imageurl=imageurl)
        return Response(data={"msg": "修改成功"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
            删除文章
            :param request:aid
            :return:msg status
            """
        aid = request.GET.get('aid')
        try:
            c = Artical.objects.get(aid=aid)
            c.delete()
            state = 1
            msg = '删除文章成功'
        except:
            state = 0
            msg = '删除文章失败'
        return JsonResponse(data={
            'state': state,
            'msg': msg
        })

@api_view(["GET"])
def loadArctial(request):
    """
    小组朋友圈文章
    :param request:gid
    :return:
    { "uid","content","atime","aid","name","picture", "imageurl","likeList": [{"name","content"}], "commentList": [ {"name","content"}] }  }
    """
    gid = request.GET.get('gid')
    sql_str = "select artical.uid,artical.content,artical.atime,artical.aid,User.name,User.picture,artical.imageurl " \
              "from User,artical where User.uid=artical.uid and artical.gid='" + str(gid)+"'order by artical.atime desc"
    dataInfo = artical_detail(sql_str)
    return Response(data=dataInfo, status=status.HTTP_200_OK)

@api_view(["GET"])
def getownArtical(request):
    """
    个人朋友圈文章
    :param request:id
    :return: { "uid","gid","content","atime","aid","name","picture", "imageurl","likeList": [{"name","content"}], "commentList": [ {"name","content"}] }  }
    """
    id = request.GET.get('id')
    sql_str = "select artical.gid,artical.content,artical.atime,artical.aid,artical.uid,User.name,User.picture,artical.imageurl " \
              "from User,artical where User.uid=artical.uid and artical.uid=" + str(id)
    dataInfo = artical_detail(sql_str)
    return Response(data=dataInfo, status=status.HTTP_200_OK)

@api_view(["GET"])
def getownlikeArtical(request):
    """
    自己点赞的文章
    :param request:id
    :return:{ "uid","gid","content","atime","aid","name","picture", "imageurl","likeList": [{"name","content"}], "commentList": [ {"name","content"}] }  }
    """
    id = request.GET.get('id')
    sql_str = "select artical.gid,artical.content,artical.atime,artical.aid,artical.uid,User.name,User.picture,artical.imageurl " \
              "from User,artical,likes where User.uid=artical.uid and likes.aid=artical.aid and likes.uid=" + str(id)

    dataInfo = artical_detail(sql_str)
    return Response(data=dataInfo, status=status.HTTP_200_OK)

@api_view(["GET"])
def getowncollectArtical(request):
    """
    自己收藏的文章
    :param request:id
    :return: {"uid","gid","content","atime","aid","name","picture", "imageurl","likeList": [{"name","content"}], "commentList": [ {"name","content"}] }  }
    """
    id = request.GET.get('id')
    sql_str = "select artical.gid,artical.content,artical.atime,artical.aid,artical.uid,User.name,User.picture,artical.imageurl " \
              "from User,artical,favorites where User.uid=artical.uid and favorites.aid=artical.aid and favorites.uid=" + str(
        id)
    dataInfo = artical_detail(sql_str)
    return Response(data=dataInfo, status=status.HTTP_200_OK)

class likeArtical(APIView):
    def post(self, request):
        """
        点赞接口，进行likes和notice数据库的新增
        :param request:uid aid currentime
        :return:state msg name
        """
        uid = request.data.get('uid')
        aid = request.data.get('aid')
        ltime = request.data.get('currentime')
        ncontent = '点赞'
        try:
            Likes.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ltime=ltime)
            Notice.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ntime=ltime,
                                  ncontent=ncontent)
            state = 1
            msg = '点赞成功'
        except:
            state = 0
            msg = '点赞失败'
        return JsonResponse(data={
            'state': state,
            'msg': msg,
        })

    def delete(self, request):
        """
        取消点赞
        :param request: uid aid
        :return: state msg name
        """
        id = request.GET.get('uid')
        aid = request.GET.get('aid')
        t = Likes.objects.filter(uid=User.objects.get(uid=id), aid=Artical.objects.get(aid=aid))
        # name = User.objects.filter(uid=id).values('name')[0]['name']
        if t.exists():
            t.delete()
            return Response(data={"msg": "删除点赞成功", 'state': 1})
        else:
            return Response(data={"msg": "没有此信息", 'state': 0})

class collectArtical(APIView):
    def post(self, request):
        """
        收藏接口，进行likes和notice数据库的新增
        :param request:uid aid currentime
        :return:state msg name
        """
        uid = request.data.get('uid')
        aid = request.data.get('aid')
        ftime = request.data.get('currentime')
        ncontent = '收藏'
        try:
            Favorites.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ftime=ftime)
            Notice.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ntime=ftime,
                                  ncontent=ncontent)
            state = 1
            msg = '收藏成功'
        except:
            state = 0
            msg = '收藏失败'
        return JsonResponse(data={
            'state': state,
            'msg': msg,
            'name': User.objects.filter(uid=uid).values('name')[0]['name']
        })

    def delete(self, request):
        """
        取消收藏
        :param request:uid aid
        :return:state msg name
        """
        id = request.GET.get('uid')
        aid = request.GET.get('aid')
        t = Favorites.objects.filter(uid=User.objects.get(uid=id), aid=Artical.objects.get(aid=aid))
        if t.exists():
            t.delete()
            return Response(data={"msg": "删除收藏成功", 'state': 1})
        else:
            return Response(data={"msg": "没有此信息", 'state': 0})

@api_view(["POST"])
def commentArtical(request):
    """
    评论文章
    :param request:uid aid currentime comment
    :return:state msg name
    """
    uid = request.data.get('uid')
    aid = request.data.get('aid')
    ctime = request.data.get('currentime')
    content = request.data.get('comment')
    ncontent='评论'
    try:
        Comment.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ctime=ctime,
                               content=content)
        Notice.objects.create(uid=User.objects.get(uid=uid), aid=Artical.objects.get(aid=aid), ntime=ctime,
                              ncontent=ncontent)
        state = 1
        msg = '评论成功'
    except:
        state = 0
        msg = '评论失败'
    return JsonResponse(data={
        'state': state,
        'msg': msg,
    })
