import pprint

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import Post, Text, Announcement, Article
import json


def show_name(request):
    context = {'name_list': Post.objects.all()}
    return render(request, 'web01.html', context=context)


@api_view(["POST"])
def register(request):
    pprint.pprint(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    code = request.data.get('adminCode')
    pprint.pprint(code)
    if username is None or password is None:
        pprint.pprint("error1")
        return Response({'error': 'Please provide both username and password'}, status=HTTP_200_OK)
    if User.objects.filter(username=username).exists():
        pprint.pprint("error2")
        return Response({'error': 'Username is already taken', 'code': -1}, status=status.HTTP_200_OK)
    if code == '':
        pprint.pprint("success")
        user = User.objects.create_user(username=username, password=password, is_active=0)
        return Response({'message': 'User created successfully', 'code': 1}, status=status.HTTP_201_CREATED)
    if code == "123":
        user = User.objects.create_user(username=username, password=password, is_active=0)
        user.is_staff = 1
        user.save()
        pprint.pprint("success")
        return Response({'message': 'User created successfully', 'code': 1}, status=status.HTTP_201_CREATED)
    else:
        pprint.pprint("error4")
        return Response({'error': 'Register Failed,please check your code'}, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_login(request):
    try:
        users = User.objects.all()
        for user in users:
            user.is_active = 0
            user.save()
        data = request.data
        username = data.get("name")
        password = data.get("password")
        pprint.pprint(password)
        user = User.objects.get(username=username)
        pprint.pprint(user.password)
        if password == user.password:
            user.is_active = 1  # 判断当前登陆用户
            user.save()
            users = User.objects.filter(is_active=1)
            for user_id in users:
                pprint.pprint("1")
            return Response({'message': 'login successfully', 'code': 1}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'error password!', 'code': 1}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User is not exist', 'code': -1}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_post(request):
    pprint.pprint(request.data)
    try:
        titles = request.data.get("titles")
        description = request.data.get("description")
        user = User.objects.get(is_active=1)
        post = Post.objects.create(titles=titles, description=description,user = user)
        return Response({"message": "Post created successfully", "post_id": post.post_id, 'code': 1},
                        status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_comment(request):
    try:
        data = request.data
        content = data.get("content")
        post_id = data.get("id")
        post = Post.objects.get(post_id=post_id)
        user = User.objects.get(is_active=1)
        Text.objects.create(content=content, post=post, user=user)
        return Response({"message": "Comment created successfully", 'code': 1}, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({"message": "Post not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(post_id=post_id)
        if post.user == request.user:
            post.delete()
            return Response({"message": "Post deleted successfully", 'code': 1}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Unauthorized", 'code': -1}, status=status.HTTP_401_UNAUTHORIZED)
    except Post.DoesNotExist:
        return Response({"message": "Post not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def favorite_post(request):
    try:
        pprint.pprint(request.data)
        data = request.data
        post_id = data.get("id")
        pprint.pprint(post_id)
        post = get_object_or_404(Post, post_id=post_id)
        user = User.objects.get(is_active=1)
        #pprint.pprint(user)
        post.user_favourite.add(user)
        return Response({"message": "Post favorited successfully", 'code': 1}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"message": "Post not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def show_posts(request):
    try:
        posts = Post.objects.all().values("post_id", "titles", "description")
        return Response(list(posts), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def show_favorited_posts(request):
    user = User.objects.get(is_active=1)
    try:
        posts = Post.objects.filter(user_favourite=user)
    except ObjectDoesNotExist:
        return Response({'message': 'No posts found'}, status=HTTP_404_NOT_FOUND)
    posts_list = []
    for post in posts:
        # 构建每个帖子的详细信息字典
        context = {
            'id': post.post_id,
            'title': post.titles,
            'content': post.description,
        }
        posts_list.append(context)
    # 返回包含所有帖子详细信息的 JSON 响应
    return JsonResponse(posts_list, status=200, safe=False)



@api_view(["POST"])
def remove_favorite(request):
    try:
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(post_id=post_id)
        post.user_favourite.remove(request.user)
        return Response({"message": "Post removed from favorites", 'code': 1}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"message": "Post not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def user_center(request):
    try:
        data = json.loads(request.body)
        password = data.get("password")
        request.user.set_password(password)
        request.user.save()
        return Response({"message": "Password updated successfully", 'code': 1}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_announcement(request):
    try:
        data = json.loads(request.body)
        title = data.get("titles")
        content = data.get("content")
        Announcement.objects.create(title=title, content=content)
        return Response({"message": "Announcement created successfully", 'code': 1}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def show_announcements(request):
    try:
        announcements = Announcement.objects.all().values("id", "title", "content")
        return Response(list(announcements), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def check_admin(request):
    user = User.objects.get(is_active=1)
    return Response({'message': user.is_staff}, status=status.HTTP_200_OK)


@api_view(["GET"])
def show_articles(request):
    try:
        articles = Article.objects.all().values("id", "title", "content")
        return Response(list(articles), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_article(request):
    try:
        data = request.data
        titles = data.get("titles")
        content = data.get("content")
        article = Article.objects.create(title=titles, content=content)
        return Response({"message": "Article  created successfully", "id":  article.id, 'code': 1},
                             status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_announcement(request):
    try:
        data = request.data
        id = data.get("id")
        announcement = Announcement.objects.get(id=id)
        announcement.delete()
        return Response({"message": "Announcement deleted successfully", 'code': 1}, status=status.HTTP_200_OK)

    except Announcement.DoesNotExist:
          return Response({"message": "Announcement not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
          return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_article(request):
    try:
        pprint.pprint(request.data)
        data = request.data
        id = data.get("id")
        article = Article.objects.get(id=id)

        article.delete()
        return Response({"message": "Article deleted successfully", 'code': 1}, status=status.HTTP_200_OK)

    except Article.DoesNotExist:
          return Response({"message": "Article not found", 'code': -1}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
          return Response({"message": str(e), 'code': -1}, status=status.HTTP_400_BAD_REQUEST)