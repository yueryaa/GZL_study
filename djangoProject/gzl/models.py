# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    uid = models.OneToOneField('User', models.DO_NOTHING, db_column='uid', primary_key=True)  # The composite primary key (uid, gid) found, that is not supported. The first column is selected.
    gid = models.ForeignKey('Group', models.DO_NOTHING, db_column='gid')
    msg = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'application'
        unique_together = (('uid', 'gid'),)


class Artical(models.Model):
    aid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    gid = models.ForeignKey('Group', models.DO_NOTHING, db_column='gid')
    content = models.CharField(max_length=255, blank=True, null=True)
    favorites_num = models.IntegerField(blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)
    atime = models.CharField(max_length=50)
    imageurl = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artical'


class Comment(models.Model):
    uid = models.OneToOneField('User', models.DO_NOTHING, db_column='uid', primary_key=True)  # The composite primary key (uid, aid, ctime) found, that is not supported. The first column is selected.
    aid = models.ForeignKey(Artical, models.DO_NOTHING, db_column='aid')
    content = models.CharField(max_length=255)
    ctime = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('uid', 'aid', 'ctime'),)


class Favorites(models.Model):
    uid = models.OneToOneField('User', models.DO_NOTHING, db_column='uid', primary_key=True)  # The composite primary key (uid, aid) found, that is not supported. The first column is selected.
    aid = models.ForeignKey(Artical, models.DO_NOTHING, db_column='aid')
    ftime = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorites'
        unique_together = (('uid', 'aid'),)


class Group(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number = models.IntegerField(blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')

    class Meta:
        managed = False
        db_table = 'group'


class Likes(models.Model):
    uid = models.OneToOneField('User', models.DO_NOTHING, db_column='uid', primary_key=True)  # The composite primary key (uid, aid) found, that is not supported. The first column is selected.
    aid = models.ForeignKey(Artical, models.DO_NOTHING, db_column='aid')
    ltime = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'likes'
        unique_together = (('uid', 'aid'),)


class Notice(models.Model):
    nid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    ncontent = models.CharField(max_length=20)
    ntime = models.CharField(max_length=50)
    aid = models.ForeignKey(Artical, models.DO_NOTHING, db_column='aid')

    class Meta:
        managed = False
        db_table = 'notice'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    account = models.CharField(unique=True, max_length=11)
    picture = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserGroup(models.Model):
    uid = models.OneToOneField(User, models.DO_NOTHING, db_column='uid', primary_key=True)  # The composite primary key (uid, gid) found, that is not supported. The first column is selected.
    gid = models.ForeignKey(Group, models.DO_NOTHING, db_column='gid')

    class Meta:
        managed = False
        db_table = 'user_group'
        unique_together = (('uid', 'gid'),)
