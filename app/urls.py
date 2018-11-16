from django.urls import path
from . import views

urlpatterns = [
    path('createuser', views.create_user, name='createuser'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout, name='logout'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('tweet', views.tweet, name='tweet'),
    path('readtweet', views.read_tweets, name='readtweet'),
    path('deletetweet', views.delete_tweet, name='deletetweet'),
    path('like', views.like_tweet, name='like_tweet'),
    path('unlike', views.unlike_tweet, name='unlike_tweet'),
    path('retweet', views.retweet, name='retweet'),
    path('reply', views.reply, name='reply')

]