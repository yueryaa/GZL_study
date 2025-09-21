# -*- coding: utf-8 -*-
# @Time    : 2024-01-07 15:46
# @Author  : yuer
# @FileName: Group_detail.py
# @Software: PyCharm


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from gzl.models import User, UserGroup, Group, Application
from gzl.serializers import Groupserializer, User_groupserializer, Applicationserializer

@api_view(["GET"])
def user_group(request):
    """
    返回id参加的小组
    :param request: id
    :return: msg/data(uid group_name User_name gid is_admin) status
    """
    id = request.GET.get('id')
    obj = UserGroup.objects.filter(uid=id)
    group = Group.objects.filter(uid=id)
    objg = Groupserializer(instance=group, many=True)
    all_group = [d['gid'] for d in objg.data]
    if not obj:
        return Response(data={"msg": "此学生没有参加小组"}, status=status.HTTP_404_NOT_FOUND)
    s = User_groupserializer(instance=obj, many=True)
    # 添加管理员字段
    for item in s.data:
        if (item['gid'] in all_group):
            item['is_admin']=1
        else:
            item['is_admin'] = 0
    return Response(data=s.data, status=status.HTTP_200_OK)

class User_GroupDetail(APIView):
    """
    对小组中成员进行管理
    """
    @staticmethod
    def get_object(gid):
        """
        获取usergroup对象
        :param gid:
        :return:
        """
        try:
            return UserGroup.objects.filter(gid=gid)
        except UserGroup.DoesNotExist:
            return

    def get(self, request):
        """
        查询gid小组中成员
        :param request:gid
        :return: uid group_name User_name gid
        """
        obj = self.get_object(request.GET.get("gid"))
        if not obj:
            return Response(data={"msg": "没有此小组信息"}, status=status.HTTP_404_NOT_FOUND)
        s = User_groupserializer(obj, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        删除gid小组中id成员
        :param request:gid id
        :return: msg
        """
        obj = self.get_object(request.GET.get("gid")).filter(uid=request.GET.get("id"))
        if not obj:
            return Response(data={"msg": "删除失败"})
        obj.delete()
        return Response(data={"msg": "删除成功"})

@api_view(["POST"])
def creat_group(request):
    """
    创建小组
    :param request: uid name
    :return: gid name number uid
    """
    s = Groupserializer(data=request.data)  # 这里是data = xx, return前要先调用.is_valid()
    if s.is_valid():
        s.save(number=0)
        uid = request.data.get("uid")
        UserGroup.objects.create(uid=User.objects.get(uid=uid),
                                 gid=Group.objects.get(gid=s.data.get("gid")))
        return Response(data=s.data, status=status.HTTP_201_CREATED)
    return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationDetail(APIView):
    """
    申请加入小组操作
    """
    def get(self, request):
        """
        管理员id 用于显示该管理员需要处理的申请
        :param request: id
        :return:uid group_name User_name msg gid
        """
        id = request.GET.get("id")
        obj = Group.objects.filter(uid=id)
        d = list(obj.values('gid'))
        a = []
        for it in d:
            a.append(it['gid'])
        res = Application.objects.filter(gid__in=a)
        da = Applicationserializer(instance=res, many=True)
        return Response(data=da.data)

    def post(self, request):
        """
        成员申请加入小组
        :param request:gid id
        :return:msg/status
        """
        try:
            Group.objects.get(gid=request.data.get("gid"))
            try:
                user = UserGroup.objects.get(gid=request.data.get("gid"), uid=request.data.get("id"))
                if user:
                    return Response(data={"msg": "您已在该小组内"})
            except UserGroup.DoesNotExist:
                try:
                    group = Group.objects.get(gid=request.data.get("gid"))
                    user = User.objects.get(uid=request.data.get("id"))
                    Application.objects.get(gid=group, uid=user)
                    msg = "重复发送申请，请耐心等待"
                except Application.DoesNotExist:
                    Application.objects.create(gid=group, uid=user, msg=request.data.get("msg"))
                    msg = "成功发送申请"
                return Response(data={"msg": msg})
        except Group.DoesNotExist:
            return Response(data={"msg": "不存在该小组"})


    def delete(self, request):
        """
        同意申请/拒绝申请，在申请表中删除
        :param request:id gid state
        :return:msg
        """
        try:
            obj = Application.objects.filter(gid=Group.objects.get(gid=request.GET.get("gid")),uid=User.objects.get(uid=request.GET.get("id")))
            if request.GET.get("state") == '0':
                obj.delete()
                return Response(data={"msg": "拒绝申请成功"})
            else:
                UserGroup.objects.create(uid=User.objects.get(uid=request.GET.get("id")),
                                         gid=Group.objects.get(gid=request.GET.get("gid")))
                obj.delete()
                return Response(data={"msg": "同意申请成功"})
        except Application.DoesNotExist:
            return Response(data={"msg": "没有此申请信息"})

