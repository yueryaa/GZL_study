# -*- coding: utf-8 -*-
# @Time    : 2023-12-03 13:37
# @Author  : yuer
# @FileName: serializers.py
# @Software: PyCharm

# 序列化
from rest_framework import serializers
from .models import User, Group, UserGroup, Application, Artical,Notice


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User #对应model中class
        fields='__all__'

class Noticeserializer(serializers.ModelSerializer):
    class Meta:
        model=Notice #对应model中class
        fields='__all__'

class Groupserializer(serializers.ModelSerializer):
    class Meta:
        model=Group #对应model中class
        fields='__all__'

class User_groupserializer(serializers.ModelSerializer):

    # 外键自动增加字段
    group_name= serializers.CharField(source='gid.name')
    User_name = serializers.CharField(source='uid.name')
    class Meta:
        model=UserGroup #对应model中class
        fields='__all__'

class Applicationserializer(serializers.ModelSerializer):

    # 外键自动增加字段
    group_name = serializers.CharField(source='gid.name')
    User_name = serializers.CharField(source='uid.name')

    class Meta:
        model = Application  # 对应model中class
        fields = '__all__'


class Articalserializer(serializers.ModelSerializer):

    # 外键自动增加字段
    group_name = serializers.CharField(source='gid.name')
    User_name = serializers.CharField(source='uid.name')

    class Meta:
        model = Artical  # 对应model中class
        fields = '__all__'