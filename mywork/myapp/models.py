from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    titles = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    user_favourite = models.ManyToManyField(User, blank=True)


class Announcement(models.Model):  # 公告
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    users = models.ManyToManyField(User, blank=True)  # 标记所有已读的用户


class Text(models.Model):  # 评论
    id = models.AutoField(primary_key = True)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="texts",null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="posts_texts",null=True)


class Article(models.Model):  # 文章
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length=500)



