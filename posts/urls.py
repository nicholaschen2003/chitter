from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.allPostView, name='allPostView'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.signin, name='signin'),
    path('failedSignin/', views.failedSignin, name='failedSignin'),
    path('userAuthentication/', views.userAuthentication, name='userAuthentication'),
    path('signup/', views.signup, name='signup'),
    path('makeUser/', views.makeUser, name='makeUser'),
    path('posts/', views.allPostView, name='allPostView'),
    path('posts/view/', views.allPostView, name='allPostView'),
    path('posts/logOut/', views.logOut, name='logOut'),
    path('posts/<twitterHandle>/view/', views.postView, name='postView'),
    path('posts/<twitterHandle>/', views.posterView, name='posterView'),
    path('posts/<twitterHandle>/<int:post_id>/', views.specificView, name='specificView'),
    path('posts/<twitterHandle>/new/', views.new, name='new'),
    path('posts/<twitterHandle>/createNewPost/', views.createNewPost, name='createNewPost'),
    path('posts/<twitterHandle>/<int:post_id>/retweet/', views.retweet, name='retweet'),
    path('posts/<twitterHandle>/<int:post_id>/reply/', views.reply, name='reply'),
    path('posts/<int:post_id>/like/', views.like, name='like'),
    path('posts/<twitterHandle>/<int:post_id>/makeRetweet/', views.makeRetweet, name='makeRetweet'),
    path('posts/<twitterHandle>/<int:post_id>/makeReply/', views.makeReply, name='makeReply'),
    path('posts/<twitterHandle>/<int:post_id>/<currentPage>/like/', views.like, name='like'),
]
